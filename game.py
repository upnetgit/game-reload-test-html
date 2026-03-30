import random
import time
import re

class RouletteGame:
    def __init__(self, mode, config):
        self.mode = mode
        self.config = config
        self.gun = []
        self.p1 = []
        self.p2 = []
        self.thing1 = config['game']['initial_items']['player1'][:]
        self.thing2 = config['game']['initial_items']['player2'][:]
        self.single = {1: 1, 2: 1}
        self.damage = {1: 1}
        self.current_player = 1
        self.winner = None
        self.message = ""
        self.show_gun_details = False
        self.epinephrine_active = False
        self.epinephrine_player = None
        self.epinephrine_items = []
        self.history = []
        self.full_history = []
        self.remane = 0
        self.last_action_used_glasses = False
        self.last_action_used_phone = False
        self.bullet_count_on_last_glasses = None
        self._init_game()

    def _init_game(self):
        health_range = self.config['game']['health_range']
        r = random.randint(health_range[0], health_range[1])
        self.p1 = ['*'] * r
        self.p2 = ['*'] * r
        self._lockon()
        self._get_items()
        self.message = "游戏开始！"
        self._record(self.message)

    def _lockon(self):
        bullet_range = self.config['game']['bullet_range']
        b = random.randint(bullet_range[0], bullet_range[1])
        self.gun = ['0'] * (b // 2) + ['1'] * (b - b // 2)
        for _ in range(random.randint(1, 4)):
            random.shuffle(self.gun)
        msg = f"\n装填了 {b} 发子弹（{self.gun.count('1')}红/{self.gun.count('0')}黑）"
        self._record(msg)
        self.show_gun_details = True

    def reset_gun_details(self):
        self.show_gun_details = False

    def _get_items(self):
        items_range = self.config['game']['items_per_round_range']
        n = random.randint(items_range[0], items_range[1])
        item_pool = self.config['game']['item_pool']
        get1 = random.choices(item_pool, k=n)
        get2 = random.choices(item_pool, k=n)
        max_items = self.config['game']['max_items']
        if len(self.thing1) < max_items:
            self.thing1.extend(get1)
        if len(self.thing2) < max_items:
            self.thing2.extend(get2)

    def _lose_item(self, player, item):
        if player == 1:
            self.thing1.remove(item)
        else:
            self.thing2.remove(item)

    def _add_item(self, player, item):
        if player == 1:
            self.thing1.append(item)
        else:
            self.thing2.append(item)

    def _record(self, msg, full_msg=None):
        if full_msg is None:
            full_msg = msg
        if not self.winner and ("手机" in msg or "放大镜" in msg):
            if "红色" in msg or "黑色" in msg:
                match = re.search(r'玩家 (\d+)', msg)
                player = match.group(1) if match else "?"
                if "手机" in msg:
                    simple_msg = f"玩家 {player} 使用了手机。"
                else:
                    simple_msg = f"玩家 {player} 使用了放大镜。"
                self.message = simple_msg
                self.history.append(simple_msg)
                self.full_history.append(full_msg)
                return
        self.message = msg
        self.history.append(msg)
        self.full_history.append(full_msg)

    def _get_item_use_func(self, item_id):
        func_map = {
            1: self.use_knife,
            2: self.use_beer,
            3: self.use_handcuffs,
            4: self.use_glasses,
            5: self.use_smoke,
            6: self.use_phone,
            7: self.use_epinephrine
        }
        return func_map.get(item_id)

    # ================== 道具效果 ==================
    def use_knife(self, player):
        if self.damage[1] == 1:
            self.damage[1] = 2
            self._lose_item(player, 1)
            msg = f"玩家 {player} 使用了刀，下次红色子弹伤害翻倍！"
            self._record(msg)
            return msg
        else:
            msg = "刀已生效，不能重复使用！"
            self._record(msg)
            return msg

    def use_beer(self, player):
        if not self.gun:
            msg = "没有子弹了！"
            self._record(msg)
            return msg
        bullet = self.gun.pop(0)
        color = "红色实弹" if bullet == '1' else "黑色空包弹"
        self._lose_item(player, 2)
        self.show_gun_details = False
        msg = f"玩家 {player} 使用了啤酒，移除的子弹是 {color}。"
        self._record(msg)
        self._reset_glasses_flag()
        return msg

    def use_handcuffs(self, player):
        opponent = 2 if player == 1 else 1
        if self.single[opponent] == 3:
            msg = "对方下一回合已被跳过，不能连续使用手铐！"
            self._record(msg)
            return msg
        self.single[opponent] = 3
        self._lose_item(player, 3)
        msg = f"玩家 {player} 使用了手铐，对方下一次获得行动权时将被跳过。"
        self._record(msg)
        return msg

    def use_glasses(self, player):
        if not self.gun:
            msg = "没有子弹了！"
            self._record(msg)
            return msg
        color = "红色实弹" if self.gun[0] == '1' else "黑色空包弹"
        self._lose_item(player, 4)
        msg = f"玩家 {player} 使用了放大镜，当前子弹是 {color}。"
        self._record(msg)
        return msg

    def use_smoke(self, player):
        max_health = self.config['game']['max_health']
        life = self.p1 if player == 1 else self.p2
        if len(life) < max_health:
            life.append('*')
            self._lose_item(player, 5)
            msg = f"玩家 {player} 使用了烟，恢复1点生命，现在生命 {len(life)}。"
            self._record(msg)
            return msg
        else:
            msg = "生命已满，无法使用烟。"
            self._record(msg)
            return msg

    def use_phone(self, player):
        if not self.gun:
            msg = "没有子弹了！"
            self._record(msg)
            return msg
        idx = random.randint(0, len(self.gun)-1)
        color = "红色实弹" if self.gun[idx] == '1' else "黑色空包弹"
        self._lose_item(player, 6)
        msg = f"玩家 {player} 使用了手机，第 {idx+1} 发子弹是 {color}。"
        self._record(msg)
        self.remane = len(self.gun) - idx
        return msg

    def use_epinephrine(self, player):
        return "epinephrine_need_choice"

    def steal_and_use(self, player, stolen_item):
        opponent = 2 if player == 1 else 1
        if opponent == 1:
            if stolen_item not in self.thing1:
                return "对方没有该道具！"
            self.thing1.remove(stolen_item)
        else:
            if stolen_item not in self.thing2:
                return "对方没有该道具！"
            self.thing2.remove(stolen_item)
        self._add_item(player, stolen_item)

        if stolen_item == 7:
            m = self.p1 if player == 1 else self.p2
            if m:
                m.pop()
            msg1 = f"玩家 {player} 偷取了肾上腺素，损失1点生命！"
            self._record(msg1)
            target_items = self.thing1 if opponent == 1 else self.thing2
            if target_items:
                second_stolen = random.choice(target_items)
                if opponent == 1:
                    self.thing1.remove(second_stolen)
                else:
                    self.thing2.remove(second_stolen)
                self._add_item(player, second_stolen)
                use_func = self._get_item_use_func(second_stolen)
                if use_func:
                    msg2 = use_func(player)
                    return f"{msg1} {msg2}"
                else:
                    msg2 = f"偷取并使用了 {second_stolen}，但效果未知。"
                    self._record(msg2)
                    return f"{msg1} {msg2}"
            else:
                msg = "对方没有其他道具可偷，肾上腺素效果无效。"
                self._record(msg)
                return msg
        else:
            use_func = self._get_item_use_func(stolen_item)
            if use_func:
                msg = use_func(player)
                return msg
            else:
                msg = f"偷取并使用了 {stolen_item}，但效果未知。"
                self._record(msg)
                return msg

    def epinephrine_timeout(self, player):
        m = self.p1 if player == 1 else self.p2
        if m:
            m.pop()
        self._lose_item(player, 7)
        msg = f"玩家 {player} 使用肾上腺素超时，损失1点生命！"
        self._record(msg)
        return msg

    # ================== 开枪逻辑 ==================
    def shoot(self, player, target):
        if not self.gun:
            msg = "没有子弹了，请先装填（将自动装填）。"
            self._record(msg)
            return msg
        bullet = self.gun.pop(0)
        is_red = bullet == '1'
        damage = self.damage[1] if is_red else 0
        self.damage[1] = 1
        self.show_gun_details = False

        opponent = 2 if player == 1 else 1

        if target == player:
            if is_red:
                life = self.p1 if player == 1 else self.p2
                for _ in range(damage):
                    if life:
                        life.pop()
                msg = f"玩家 {player} 对自己开枪，子弹是红色，受到 {damage} 点伤害！"
            else:
                msg = f"玩家 {player} 对自己开枪，子弹是黑色，无伤害。"
        else:
            life = self.p1 if opponent == 1 else self.p2
            if is_red:
                for _ in range(damage):
                    if life:
                        life.pop()
                msg = f"玩家 {player} 对玩家 {opponent} 开枪，子弹是红色，造成 {damage} 点伤害！"
            else:
                msg = f"玩家 {player} 对玩家 {opponent} 开枪，子弹是黑色，无伤害。"

        self._record(msg)

        if len(self.p1) == 0:
            self.winner = 2
            self._record("玩家2获胜！")
            return "game_over"
        if len(self.p2) == 0:
            self.winner = 1
            self._record("玩家1获胜！")
            return "game_over"

        if is_red:
            next_player = opponent
        else:
            if target == opponent:
                next_player = opponent
            else:
                next_player = player

        if self.single[next_player] == 3:
            self.single[next_player] = 2
            msg += f" 由于手铐效果，玩家 {next_player} 被跳过，玩家 {player} 继续行动。"
            next_player = player
        elif self.single[next_player] == 2:
            self.single[next_player] = 1

        self.current_player = next_player

        if len(self.gun) == 0:
            self._lockon()
            self._get_items()
            msg += "\n弹匣已空，重新装填并补充道具。"

        return msg

    # ================== AI 决策辅助方法 ==================
    def _reset_glasses_flag(self):
        self.last_action_used_glasses = False
        self.bullet_count_on_last_glasses = None

    def _ai_ifr(self):
        if random.random() < 0.8 and 1 in self.thing1 and 7 in self.thing2 and self.damage[1] == 1:
            self.steal_and_use(2, 1)
            self.shoot(2, 1)
        elif 1 in self.thing2 and 7 not in self.thing2 and 1 not in self.thing1 and self.damage[1] == 1:
            self.use_knife(2)
            self.shoot(2, 1)
        else:
            self.shoot(2, 1)

    def _ai_ifb(self):
        if random.random() < 0.5 and 2 in self.thing2:
            self.use_beer(2)
        elif 2 not in self.thing2 and 2 in self.thing1 and 7 in self.thing2:
            self.steal_and_use(2, 2)
        self.shoot(2, 2)

    def ai_step(self):
        time.sleep(1)  # 新增：AI 思考延迟 1 秒
        if self.winner or self.current_player != 2:
            return False, None

        r = self.gun.count('1')
        b = self.gun.count('0')
        a = len(self.gun)
        pr = r / a if a > 0 else 0
        pb = b / a if a > 0 else 0

        max_health = self.config['game']['max_health']
        for _ in range(1, 6):
            current_health = len(self.p2)
            if current_health < max_health and 5 in self.thing2:
                self.use_smoke(2)
                if self.winner or self.current_player != 2:
                    return False, self.message
                return True, self.message
            elif current_health < max_health and 5 in self.thing1 and 7 in self.thing2:
                prob = (max_health - current_health) / max_health * 0.6
                if random.random() < prob:
                    self.steal_and_use(2, 5)
                    if self.winner or self.current_player != 2:
                        return False, self.message
                    return True, self.message

        p = random.random()

        # 放大镜
        if p > 0.9:
            can_use_glasses = False
            if 4 in self.thing2:
                can_use_glasses = True
            elif 4 in self.thing1 and 7 in self.thing2:
                can_use_glasses = True
            if can_use_glasses and (not self.last_action_used_glasses or len(self.gun) != self.bullet_count_on_last_glasses):
                if 4 in self.thing2:
                    self.use_glasses(2)
                else:
                    self.steal_and_use(2, 4)
                self.last_action_used_glasses = True
                self.bullet_count_on_last_glasses = len(self.gun)
                self.last_action_used_phone = False
                if self.winner or self.current_player != 2:
                    return False, self.message
                if self.gun and self.gun[0] == '1':
                    self._ai_ifr()
                else:
                    self._ai_ifb()
                if self.winner or self.current_player != 2:
                    return False, self.message
                return True, self.message

        # 手铐
        if p > 0.7:
            can_use_handcuffs = False
            if 3 in self.thing2 and self.single[1] == 1:
                can_use_handcuffs = True
            elif 3 in self.thing1 and 7 in self.thing2 and self.single[1] == 1:
                can_use_handcuffs = True
            if can_use_handcuffs:
                if 3 in self.thing2:
                    self.use_handcuffs(2)
                else:
                    self.steal_and_use(2, 3)
                self.last_action_used_glasses = False
                self.last_action_used_phone = False
                if self.winner or self.current_player != 2:
                    return False, self.message
                return True, self.message

        # 手机
        if p > 0.5 and not self.last_action_used_phone:
            can_use_phone = False
            if 6 in self.thing2:
                can_use_phone = True
            elif 6 in self.thing1 and 7 in self.thing2:
                can_use_phone = True
            if can_use_phone:
                if 6 in self.thing2:
                    self.use_phone(2)
                else:
                    self.steal_and_use(2, 6)
                self.last_action_used_phone = True
                self.last_action_used_glasses = False
                if self.winner or self.current_player != 2:
                    return False, self.message
                return True, self.message

        # 啤酒
        if p > 0.3:
            can_use_beer = False
            if 2 in self.thing2:
                can_use_beer = True
            elif 2 in self.thing1 and 7 in self.thing2:
                can_use_beer = True
            if can_use_beer:
                if 2 in self.thing2:
                    self.use_beer(2)
                else:
                    self.steal_and_use(2, 2)
                self.last_action_used_glasses = False
                self.last_action_used_phone = False
                if self.winner or self.current_player != 2:
                    return False, self.message
                return True, self.message

        # 开枪
        if self.remane == len(self.gun):
            if self.gun and self.gun[0] == '1':
                self._ai_ifr()
            else:
                self._ai_ifb()
            self.remane = 0
            self.last_action_used_glasses = False
            self.last_action_used_phone = False
        else:
            if pr > pb:
                self._ai_ifr()
            elif pr > p and pr < pb:
                self._ai_ifb()
            else:
                if random.random() < 0.5:
                    self._ai_ifr()
                else:
                    self._ai_ifb()
            self.last_action_used_glasses = False
            self.last_action_used_phone = False

        if self.winner or self.current_player != 2:
            return False, self.message
        else:
            return True, self.message

    # ================== 状态获取 ==================
    def get_state(self):
        if self.winner:
            history_to_return = self.full_history[-10:]
        else:
            history_to_return = self.history[-10:]

        return {
            "mode": self.mode,
            "current_player": self.current_player,
            "winner": self.winner,
            "message": self.message,
            "p1_life": len(self.p1),
            "p2_life": len(self.p2),
            "p1_items": {item: self.thing1.count(item) for item in set(self.thing1)},
            "p2_items": {item: self.thing2.count(item) for item in set(self.thing2)},
            "gun_red": self.gun.count('1'),
            "gun_black": self.gun.count('0'),
            "damage_multiplier": self.damage[1],
            "show_gun_details": self.show_gun_details,
            "history": history_to_return
        }