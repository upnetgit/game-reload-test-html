# <font style="color:rgb(15, 17, 21);">俄罗斯轮盘双人对战游戏（Web版）</font>
<font style="color:rgb(15, 17, 21);">这是一个基于 Flask 框架的网页版俄罗斯轮盘游戏，融合了策略与运气，支持</font>**<font style="color:rgb(15, 17, 21);">玩家对战（PVP）</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">和</font>**<font style="color:rgb(15, 17, 21);">玩家 vs AI（PVE）</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">两种模式。游戏包含多种道具，AI 具备智能决策能力，所有操作实时同步，界面直观。</font>

---

## <font style="color:rgb(15, 17, 21);">🎮</font><font style="color:rgb(15, 17, 21);"> 游戏规则</font>
+ <font style="color:rgb(15, 17, 21);">两名玩家初始拥有</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">2~6 点随机生命值</font>**<font style="color:rgb(15, 17, 21);">（用 </font><font style="color:rgb(15, 17, 21);">❤️</font><font style="color:rgb(15, 17, 21);"> 表示）。</font>
+ <font style="color:rgb(15, 17, 21);">每回合开始前，系统会随机装填</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">2~8 发子弹</font>**<font style="color:rgb(15, 17, 21);">（红色实弹</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">1</font>`<font style="color:rgb(15, 17, 21);">，黑色空包弹</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">0</font>`<font style="color:rgb(15, 17, 21);">），并随机打乱顺序。</font>
+ <font style="color:rgb(15, 17, 21);">每回合开始时，双方会随机获得</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">2~4 个道具</font>**<font style="color:rgb(15, 17, 21);">（上限 8 个）。</font>
+ <font style="color:rgb(15, 17, 21);">玩家在自己的回合内可以：</font>
    - **<font style="color:rgb(15, 17, 21);">使用道具</font>**<font style="color:rgb(15, 17, 21);">（点击道具按钮）</font>
    - **<font style="color:rgb(15, 17, 21);">直接开枪</font>**<font style="color:rgb(15, 17, 21);">（选择向自己或向对方开枪）</font>
+ <font style="color:rgb(15, 17, 21);">开枪结果：</font>
    - **<font style="color:rgb(15, 17, 21);">红色子弹</font>**<font style="color:rgb(15, 17, 21);">：对目标造成 1 点伤害（若已使用刀，则伤害翻倍），之后</font>**<font style="color:rgb(15, 17, 21);">交换回合</font>**<font style="color:rgb(15, 17, 21);">。</font>
    - **<font style="color:rgb(15, 17, 21);">黑色子弹</font>**<font style="color:rgb(15, 17, 21);">：无伤害，</font>**<font style="color:rgb(15, 17, 21);">当前玩家可继续行动</font>**<font style="color:rgb(15, 17, 21);">（回合不结束）。</font>
+ <font style="color:rgb(15, 17, 21);">当一方生命值归零时，游戏结束，另一方获胜。</font>

---

## <font style="color:rgb(15, 17, 21);">🧰</font><font style="color:rgb(15, 17, 21);"> 道具列表及效果</font>
| <font style="color:rgb(15, 17, 21);">编号</font> | <font style="color:rgb(15, 17, 21);">名称</font> | <font style="color:rgb(15, 17, 21);">效果</font> |
| --- | --- | --- |
| <font style="color:rgb(15, 17, 21);">1</font> | <font style="color:rgb(15, 17, 21);">knife</font> | <font style="color:rgb(15, 17, 21);">使下一次红色子弹伤害翻倍（伤害=2），使用后立即生效，开枪后重置。</font> |
| <font style="color:rgb(15, 17, 21);">2</font> | <font style="color:rgb(15, 17, 21);">beer</font> | <font style="color:rgb(15, 17, 21);">移除当前子弹并查看其颜色，</font>**<font style="color:rgb(15, 17, 21);">不结束回合</font>**<font style="color:rgb(15, 17, 21);">（玩家可继续行动）。</font> |
| <font style="color:rgb(15, 17, 21);">3</font> | <font style="color:rgb(15, 17, 21);">handcuffs</font> | <font style="color:rgb(15, 17, 21);">使对方</font>**<font style="color:rgb(15, 17, 21);">下一次获得行动权时被跳过</font>**<font style="color:rgb(15, 17, 21);">。</font>**<font style="color:rgb(15, 17, 21);">不能连续两回合对同一人使用</font>**<font style="color:rgb(15, 17, 21);">。</font> |
| <font style="color:rgb(15, 17, 21);">4</font> | <font style="color:rgb(15, 17, 21);">glasses</font> | <font style="color:rgb(15, 17, 21);">查看当前子弹的颜色（不消耗子弹）。</font> |
| <font style="color:rgb(15, 17, 21);">5</font> | <font style="color:rgb(15, 17, 21);">smoke</font> | <font style="color:rgb(15, 17, 21);">回复 1 点生命值（上限 6 点）。</font> |
| <font style="color:rgb(15, 17, 21);">6</font> | <font style="color:rgb(15, 17, 21);">phone</font> | <font style="color:rgb(15, 17, 21);">随机查看一颗子弹的颜色（不消耗子弹）。</font> |
| <font style="color:rgb(15, 17, 21);">7</font> | <font style="color:rgb(15, 17, 21);">epinephrine</font> | **<font style="color:rgb(15, 17, 21);">偷取对方的某个道具并立即使用</font>**<font style="color:rgb(15, 17, 21);">。使用后有 3 秒倒计时，需选择道具编号；超时则损失 1 点生命。</font> |


<font style="color:rgb(15, 17, 21);">手机和放大镜的结果在游戏过程中仅显示“使用了手机/放大镜”，详细结果会在</font>**<font style="color:rgb(15, 17, 21);">结算页面</font>**<font style="color:rgb(15, 17, 21);">完整显示。</font>

---

## <font style="color:rgb(15, 17, 21);">🎯</font><font style="color:rgb(15, 17, 21);"> 游戏模式</font>
+ **<font style="color:rgb(15, 17, 21);">1 - PVP（双人对战）</font>**<font style="color:rgb(15, 17, 21);">：两名玩家轮流手动操作。</font>
+ **<font style="color:rgb(15, 17, 21);">2 - PVE（人机对战）</font>**<font style="color:rgb(15, 17, 21);">：玩家 1 手动操作，玩家 2 由 AI 控制。</font>

<font style="color:rgb(15, 17, 21);">AI 决策逻辑基于原控制台版本，包含以下行为：</font>

+ <font style="color:rgb(15, 17, 21);">优先使用烟恢复生命（生命值越低，偷取对方烟的概率越高，最高 0.6）。</font>
+ <font style="color:rgb(15, 17, 21);">根据随机概率使用放大镜、手铐、手机、啤酒等道具，优先级：</font>**<font style="color:rgb(15, 17, 21);">放大镜 > 手铐 > 手机 > 啤酒</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ <font style="color:rgb(15, 17, 21);">在红色子弹时，有概率使用刀增加伤害。</font>
+ <font style="color:rgb(15, 17, 21);">在黑色子弹时，有概率使用啤酒跳过当前子弹。</font>
+ <font style="color:rgb(15, 17, 21);">每次行动前有</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">1 秒</font>**<font style="color:rgb(15, 17, 21);">后端延迟，前端轮询间隔</font><font style="color:rgb(15, 17, 21);"> </font>**<font style="color:rgb(15, 17, 21);">1 秒</font>**<font style="color:rgb(15, 17, 21);">，使玩家能看清 AI 的每步操作。</font>

---

## <font style="color:rgb(15, 17, 21);">🛠️</font><font style="color:rgb(15, 17, 21);"> 技术栈</font>
+ **<font style="color:rgb(15, 17, 21);">后端</font>**<font style="color:rgb(15, 17, 21);">：Python 3 + Flask（轻量级 Web 框架）</font>
+ **<font style="color:rgb(15, 17, 21);">前端</font>**<font style="color:rgb(15, 17, 21);">：HTML5 + CSS3 + JavaScript（原生，无外部库）</font>
+ **<font style="color:rgb(15, 17, 21);">配置管理</font>**<font style="color:rgb(15, 17, 21);">：YAML 文件（可自定义游戏参数）</font>
+ **<font style="color:rgb(15, 17, 21);">状态存储</font>**<font style="color:rgb(15, 17, 21);">：内存字典 + Flask Session</font>

---

## <font style="color:rgb(15, 17, 21);">📁</font><font style="color:rgb(15, 17, 21);"> 项目结构</font>
<font style="color:rgb(15, 17, 21);">text</font>

```plain
project/
├── app.py                 # Flask 主应用
├── game.py                # 游戏核心逻辑类
├── config.yaml            # 配置文件（道具池、生命值范围等）
├── requirements.txt       # Python 依赖
└── templates/
    ├── index.html         # 游戏主页面
    └── result.html        # 结算页面（展示完整历史）
```

---

## <font style="color:rgb(15, 17, 21);">🚀</font><font style="color:rgb(15, 17, 21);"> 安装与运行</font>
### <font style="color:rgb(15, 17, 21);">1. 环境要求</font>
+ <font style="color:rgb(15, 17, 21);">Python 3.7+</font>
+ <font style="color:rgb(15, 17, 21);">pip</font>

### <font style="color:rgb(15, 17, 21);">2. 安装依赖</font>
<font style="color:rgb(15, 17, 21);">bash</font>

<font style="color:rgb(15, 17, 21);">pip install flask pyyaml</font>

### <font style="color:rgb(15, 17, 21);">3. 启动服务</font>
<font style="color:rgb(15, 17, 21);">bash</font>

<font style="color:rgb(15, 17, 21);">python app.py</font>

### <font style="color:rgb(15, 17, 21);">4. 访问游戏</font>
<font style="color:rgb(15, 17, 21);">打开浏览器，访问</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">http://127.0.0.1:5000/</font>`<font style="color:rgb(15, 17, 21);">，选择模式开始游戏。</font>

---

## <font style="color:rgb(15, 17, 21);">⚙️</font><font style="color:rgb(15, 17, 21);"> 配置文件说明</font>
`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">config.yaml</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">允许您调整游戏参数，无需修改代码：</font>

<font style="color:rgb(15, 17, 21);">yaml</font>

```plain
game:
  item_pool: [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,1,2,3,5,5,7,7,7]
  initial_items:
    player1: [3]   # 玩家1初始道具（手铐）
    player2: [6]   # 玩家2初始道具（手机）
  health_range: [2, 6]      # 初始生命值范围
  bullet_range: [2, 8]      # 每次装填子弹数量范围
  items_per_round_range: [2, 4]  # 每轮获得道具数量范围
  max_items: 8               # 道具上限
  max_health: 6              # 生命值上限
```

---

## <font style="color:rgb(15, 17, 21);">📦</font><font style="color:rgb(15, 17, 21);"> 代码结构概览</font>
### `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">game.py</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">– 游戏核心类</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">RouletteGame</font>`
+ **<font style="color:rgb(15, 17, 21);">初始化</font>**<font style="color:rgb(15, 17, 21);">：设置生命、装弹、道具。</font>
+ **<font style="color:rgb(15, 17, 21);">道具效果函数</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">use_knife</font>`<font style="color:rgb(15, 17, 21);">,</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">use_beer</font>`<font style="color:rgb(15, 17, 21);">,</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">use_handcuffs</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">等，每个函数记录消息并更新状态。</font>
+ **<font style="color:rgb(15, 17, 21);">开枪逻辑</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">shoot()</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">判断子弹颜色、伤害、手铐效果，切换玩家，自动重装。</font>
+ **<font style="color:rgb(15, 17, 21);">AI 决策</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">ai_step()</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">逐步执行 AI 行为，支持优先级、道具偷取、概率决策。</font>
+ **<font style="color:rgb(15, 17, 21);">历史记录</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">_record()</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">在游戏过程中隐藏手机/放大镜细节，结算时显示完整历史。</font>
+ **<font style="color:rgb(15, 17, 21);">状态获取</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">get_state()</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">返回当前状态供前端渲染。</font>

### `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">app.py</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">– Flask 路由</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/</font>`<font style="color:rgb(15, 17, 21);">：首页（模式选择）</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/start</font>`<font style="color:rgb(15, 17, 21);">：创建新游戏实例</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/game</font>`<font style="color:rgb(15, 17, 21);">：游戏主页面</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/result</font>`<font style="color:rgb(15, 17, 21);">：结算页面</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/api/status</font>`<font style="color:rgb(15, 17, 21);">：获取当前状态</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/api/action</font>`<font style="color:rgb(15, 17, 21);">：处理玩家操作（使用道具、开枪、肾上腺素偷取等）</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/api/ai_step</font>`<font style="color:rgb(15, 17, 21);">：执行一步 AI 动作，返回是否继续</font>
+ `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/api/reset_gun_details</font>`<font style="color:rgb(15, 17, 21);">：重置弹匣详细显示标志</font>

### `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">templates/index.html</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">– 游戏界面</font>
+ <font style="color:rgb(15, 17, 21);">实时显示玩家生命、道具、弹匣、消息和历史记录。</font>
+ <font style="color:rgb(15, 17, 21);">通过</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">setInterval</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">轮询状态（2 秒）。</font>
+ <font style="color:rgb(15, 17, 21);">AI 回合时启动轮询，每次请求</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">/api/ai_step</font>`<font style="color:rgb(15, 17, 21);">，间隔 1 秒。</font>
+ <font style="color:rgb(15, 17, 21);">肾上腺素模态框（3 秒倒计时选择偷取道具）。</font>
+ <font style="color:rgb(15, 17, 21);">自动滚动历史记录到最新消息。</font>

### `<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">templates/result.html</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">– 结算页面</font>
+ <font style="color:rgb(15, 17, 21);">显示获胜者、最终生命值、</font>**<font style="color:rgb(15, 17, 21);">完整操作历史</font>**<font style="color:rgb(15, 17, 21);">（包括手机/放大镜的详细结果）。</font>
+ <font style="color:rgb(15, 17, 21);">提供“重新开始”和“返回首页”按钮。</font>

---

## <font style="color:rgb(15, 17, 21);">🔧</font><font style="color:rgb(15, 17, 21);"> 自定义与调试</font>
+ **<font style="color:rgb(15, 17, 21);">修改 AI 行为</font>**<font style="color:rgb(15, 17, 21);">：调整</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">ai_step</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">中的概率阈值或优先级顺序。</font>
+ **<font style="color:rgb(15, 17, 21);">调整延迟</font>**<font style="color:rgb(15, 17, 21);">：修改</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">game.py</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">中</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">ai_step</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">的</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">time.sleep(1)</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">和前端</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">setTimeout</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">的数值。</font>
+ **<font style="color:rgb(15, 17, 21);">增加历史显示条数</font>**<font style="color:rgb(15, 17, 21);">：在</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">get_state</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">中更改</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">self.history[-10:]</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">的数字。</font>
+ **<font style="color:rgb(15, 17, 21);">清空历史</font>**<font style="color:rgb(15, 17, 21);">：游戏重置时会自动清空历史记录。</font>
+ **<font style="color:rgb(15, 17, 21);">调试模式</font>**<font style="color:rgb(15, 17, 21);">：</font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">app.py</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">已开启</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">debug=True</font>`<font style="color:rgb(15, 17, 21);">，便于开发。</font>

---

## <font style="color:rgb(15, 17, 21);">📝</font><font style="color:rgb(15, 17, 21);"> 注意事项</font>
+ <font style="color:rgb(15, 17, 21);">游戏状态存储在服务器内存中，</font>**<font style="color:rgb(15, 17, 21);">重启服务会丢失所有游戏实例</font>**<font style="color:rgb(15, 17, 21);">。</font>
+ <font style="color:rgb(15, 17, 21);">不同浏览器标签页共享同一会话（基于 Flask Session），如需独立游戏请修改 session 机制。</font>
+ <font style="color:rgb(15, 17, 21);">肾上腺素超时逻辑：前端倒计时结束后发送</font><font style="color:rgb(15, 17, 21);"> </font>`<font style="color:rgb(15, 17, 21);background-color:rgb(235, 238, 242);">epinephrine_timeout</font>`<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">请求，后端扣除 1 点生命并移除肾上腺素道具。</font>
+ <font style="color:rgb(15, 17, 21);">偷取肾上腺素：如果偷取的道具是肾上腺素，则先损失 1 点生命，然后随机偷取对方另一个道具并立即使用。</font>
+ <font style="color:rgb(15, 17, 21);">手机和放大镜的详细结果仅在结算页面显示，游戏过程中隐藏以增加悬念。</font>

---

## <font style="color:rgb(15, 17, 21);">👤</font><font style="color:rgb(15, 17, 21);"> 作者</font>
<font style="color:rgb(15, 17, 21);">allenalla  
</font><font style="color:rgb(15, 17, 21);">（项目基于 Python 控制台版重构，代码仅供学习交流）</font>

**<font style="color:rgb(15, 17, 21);">Enjoy the game!</font>**<font style="color:rgb(15, 17, 21);"> </font><font style="color:rgb(15, 17, 21);">🎲🔫</font>

