from flask import jsonify, request, Response

from . import api
from .. import db
from ..models.player import Player
from ..models import player_marshaller, score_marshaller
from ..schemas.player import player_schema, players_schema
from flask.ext.restful import marshal

def error(msg, status=400):
    resp = jsonify({'error':msg})
    resp.status_code = status
    return resp

@api.route('/players', methods=['GET'])
def get_players():
    return jsonify({'players': marshal(Player.query.all(), player_marshaller)})

@api.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.filter_by(id=id).first()
    if player is not None:
        return jsonify(marshal(player, player_marshaller))
    else:
        return error("Not found.", 404)

@api.route('/players/find', methods=['GET'])
def find_player():
    if 'device_id' in request.args:
        device_id = request.args['device_id']
        player = Player.query.filter_by(device_id=device_id)
        if 'name' in request.args:
            name = request.args['name']
            player = player.filter_by(name=name)
        players = player.all()
        if len(players) == 0:
            return error("Not found.", 404)
        return jsonify({'results': marshal(players, player_marshaller)})
    else:
        return error("You must include 'device_id' and 'name' in your query.")

@api.route('/players', methods=['POST'])
def create_player():
    if 'device_id' in request.args and 'name' in request.args:
        device_id = request.args['device_id']
        name = request.args['name']
        player = Player.query.filter_by(device_id=device_id).filter_by(name=name).first
        if player is not None:
            player = Player(device_id, name)
            player.save()
        return jsonify(marshal(player, player_marshaller))
    else:
        return error("You must include 'device_id' and 'name' in your query.")

@api.route('/players/<int:id>/hifives', methods=['POST','PUT'])
def set_hifives(id):
    player = Player.query.filter_by(id=id).first()
    if player is not None:
        if 'hifives' in request.args:
            try:
                hifives = int(request.args['hifives'])
                player.hifives = hifives
                player.save()
            except e:
                return error("'hifives' must be an integer.")
        else:
            return error("'hifives' must be provided in request.")
        return jsonify(marshal(player, player_marshaller))
    else:
        return error("Not found.", 404)

@api.route('/players/<int:id>/characters', methods=['POST','PUT'])
def set_characters(id):
    player = Player.query.filter_by(id=id).first()
    if player is not None:
        if 'characters' in request.args:
            try:
                characters = int(request.args['characters'])
                player.characters = characters
                player.save()
            except e:
                return error("'characters' must be an integer.")
        else:
            return error("'characters' must provided in request.")
        return jsonify(marshal(player, player_marshaller))
    else:
        return error("Not found.", 404)

@api.route('/players/<int:id>/scores', methods=['GET'])
def get_player_scores(id):
    player = Player.query.filter_by(id=id).first()
    if player is not None:
        scores = sorted(player.scores, key=lambda x: -x.score)
        limit = 15
        if 'limit' in request.args:
            try:
                limit = int(request.args['limit'])
            except e:
                pass
        scores = scores[:limit]
        return jsonify({'scores': marshal(scores, score_marshaller)})
    else:
        return error("Not found.", 404)
