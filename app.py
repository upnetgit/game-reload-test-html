from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import uuid
import yaml
from game import RouletteGame

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 加载配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

games = {}

@app.route('/')
def index():
    return render_template('index.html', mode=None)

@app.route('/start', methods=['POST'])
def start_game():
    mode = int(request.form.get('mode', 1))
    if 'game_id' not in session:
        session['game_id'] = str(uuid.uuid4())
    game_id = session['game_id']
    games[game_id] = RouletteGame(mode, config)
    return redirect(url_for('game'))

@app.route('/reset')
def reset_game():
    game_id = session.get('game_id')
    if game_id and game_id in games:
        games[game_id] = RouletteGame(games[game_id].mode, config)
    return redirect(url_for('game'))

@app.route('/game')
def game():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return redirect(url_for('index'))
    game = games[game_id]
    state = game.get_state()
    return render_template('index.html', mode=state['mode'], state=state)

@app.route('/result')
def result():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return redirect(url_for('index'))
    game = games[game_id]
    winner = game.winner
    if winner is None:
        return redirect(url_for('game'))
    history = game.full_history if hasattr(game, 'full_history') else []
    p1_life = len(game.p1)
    p2_life = len(game.p2)
    return render_template('result.html', winner=winner, history=history, p1_life=p1_life, p2_life=p2_life)

@app.route('/api/status')
def status():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    game = games[game_id]
    state = game.get_state()
    return jsonify(state)

@app.route('/api/action', methods=['POST'])
def action():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    game = games[game_id]
    data = request.json
    action_type = data.get('type')
    player = data.get('player')

    if game.winner:
        return jsonify({'error': 'Game over'}), 400
    if game.current_player != player:
        return jsonify({'error': 'Not your turn'}), 400

    result = None
    if action_type == 'use_item':
        item = data.get('item')
        if item == 1:
            result = game.use_knife(player)
        elif item == 2:
            result = game.use_beer(player)
        elif item == 3:
            result = game.use_handcuffs(player)
        elif item == 4:
            result = game.use_glasses(player)
        elif item == 5:
            result = game.use_smoke(player)
        elif item == 6:
            result = game.use_phone(player)
        elif item == 7:
            if game.epinephrine_active:
                return jsonify({'error': '已经使用过肾上腺素，等待选择'}), 400
            opponent = 2 if player == 1 else 1
            target_items = game.thing1 if opponent == 1 else game.thing2
            unique_items = list(set(target_items))
            if not unique_items:
                result = "对方没有道具可偷！"
                game.message = result
                state = game.get_state()
                return jsonify({'success': True, 'state': state})
            game.epinephrine_active = True
            game.epinephrine_player = player
            game.epinephrine_items = unique_items
            state = game.get_state()
            return jsonify({'success': True, 'state': state, 'need_choice': True, 'items': unique_items})
    elif action_type == 'shoot':
        target = data.get('target')
        result = game.shoot(player, target)
    elif action_type == 'steal':
        stolen = data.get('item')
        if game.epinephrine_active and game.epinephrine_player == player:
            result = game.steal_and_use(player, stolen)
            game.epinephrine_active = False
        else:
            result = "无效的偷取请求"
    elif action_type == 'epinephrine_timeout':
        if game.epinephrine_active and game.epinephrine_player == player:
            result = game.epinephrine_timeout(player)
            game.epinephrine_active = False
        else:
            result = "无效的超时"
    else:
        return jsonify({'error': 'Invalid action'}), 400

    if result:
        game.message = result

    if game.winner:
        state = game.get_state()
        return jsonify({'success': True, 'state': state, 'game_over': True, 'redirect': url_for('result')})

    state = game.get_state()
    return jsonify({'success': True, 'state': state})

@app.route('/api/ai_step', methods=['POST'])
def ai_step():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    game = games[game_id]
    if game.mode != 2 or game.current_player != 2 or game.winner:
        return jsonify({'error': 'Not AI turn'}), 400
    cont, msg = game.ai_step()
    state = game.get_state()
    if game.winner:
        return jsonify({
            'success': True,
            'state': state,
            'game_over': True,
            'redirect': url_for('result')
        })
    return jsonify({
        'success': True,
        'state': state,
        'continue': cont,
        'message': msg
    })

@app.route('/api/reset_gun_details', methods=['POST'])
def reset_gun_details():
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    game = games[game_id]
    game.reset_gun_details()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)