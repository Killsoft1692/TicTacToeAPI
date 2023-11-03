from datetime import datetime

from flask import request, jsonify
from peewee import IntegrityError, DoesNotExist, fn, SQL

import settings
from main import app, game, game_locker, Player, Game
from decorators import is_game_ready
from errors import GameLockedError


@app.get("/game/board")
def view_board():
    return jsonify(game.get_board().tolist()), 200


@app.post("/game/move")
@is_game_ready
def register_move():
    request_data = request.get_json()
    try:
        status = game.play(request_data['row'], request_data['col'])
        return {'status': status}, 201
    except Exception as exc:
        return {'error': str(exc)}, 400


@app.get("/game/active_player")
@is_game_ready
def get_active_player():
    current_symbol = game.current_player
    active_player = Player.resolve_player_from_symbol(current_symbol)
    return {'active_player': active_player.username}, 200


@app.get("/game/statistics/<username>")
def get_players_stats(username: str):
    # query to count wins for the current player
    wins_query = Player.select(
        Player,
        fn.COUNT(Game.id).alias('win_count')
    ).join(
        Game,
        on=(Game.winner == Player.id)
    ).where(
        Player.username == username
    )
    # query to count losses for current player
    losses_query = Player.select(
        Player,
        fn.COUNT(Game.id).alias('loss_count')
    ).join(
        Game,
        on=(Game.looser == Player.id)
    ).where(
        Player.username == username
    )

    return {"win_count": wins_query.get().win_count, "loss_count": losses_query.get().loss_count}


@app.get("/game/leaderboard")
def leaderboard():
    win_query = Player.select(
        Player,
        fn.COUNT(Game.id).alias('win_count')
    ).join(
        Game,
        on=(Game.winner == Player.id)
    ).group_by(Player).order_by(SQL('win_count').desc()).limit(settings.LEADERBOARD_LIMIT)

    return [{"player": player.username, "wins": player.win_count} for player in win_query]


@app.get("/game/looserboard")
def looserboard():
    loss_query = Player.select(
        Player,
        fn.COUNT(Game.id).alias('loss_count')
    ).join(
        Game,
        on=(Game.looser == Player.id)
    ).group_by(Player).order_by(SQL('loss_count').desc()).limit(settings.LEADERBOARD_LIMIT)

    return [{"player": player.username, "loss": player.loss_count} for player in loss_query]


@app.post("/player")
def register_player():
    request_data = request.get_json()
    current_symbol = game.current_player
    try:
        game_locker.lock_player(current_symbol)
    except GameLockedError:
        return {'error': 'Apologies, but the game is currently restricted, and we\'ve already chosen two players.'}
    request_data['game_symbol'] = current_symbol
    game.switch_player()
    try:
        # Trying to create a new user
        Player.create(**request_data)
        return {"status": "Player added"}, 201
    except IntegrityError:
        # In case when user is already creates we're updating an existing one
        p = Player.select().where(Player.username == request_data['username']).get()
        p.game_symbol = current_symbol
        p.updated_at = datetime.now()
        p.save()
        return {"status": "Player selected"}, 200


@app.get("/players")
def list_all_players():
    query = Player.select(Player.id, Player.username)
    return {
               player.id: {'name': player.username,
                           'details': f'{settings.HOST}:{settings.PORT}/player/{player.id}'}
               for player in query}, 200


@app.get("/player/<player_id>")
def get_player_data(player_id):
    try:
        player = Player.get(Player.id == player_id)
    except DoesNotExist:
        return {"error": "Player not found"}, 404
    return {
                "name": player.username,
                "game_symbol": player.game_symbol,
                "stats": f'{settings.HOST}:{settings.PORT}/game/statistics/{player.username}'
           }, 200


