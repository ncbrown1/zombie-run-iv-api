from flask import jsonify, request

from . import api
from .. import db
from ..models.score import Score
from ..models import score_marshaller
from ..schemas.score import score_schema, scores_schema
from flask.ext.restful import marshal


def error(msg, status=400):
    resp = jsonify({'error':msg})
    resp.status_code = status
    return resp

@api.route('/scores', methods=['GET'])
def get_scores():
    Q = Score.query.order_by(Score.score.desc())
    limit = 15
    if 'limit' in request.args:
        try:
            limit = int(request.args['limit'])
        except e:
            pass
    Q = Q.limit(limit)
    return jsonify({'scores': marshal(Q.all(), score_marshaller)})


@api.route('/scores', methods=['POST'])
def create_score():
    if 'device_id' in request.args and 'name' in request.args and 'score' in request.args:
        try:
            score = int(request.args['score'])
            device_id = request.args['device_id']
            name = request.args['name']

            newscore = Score(score, name, device_id)
            newscore.save()

            Q = Score.query.order_by(Score.score.desc())
            rank = 1
            for s in Q.all():
                if s == newscore:
                    break
                else:
                    rank += 1
            return jsonify({"score":marshal(newscore, score_marshaller),"rank":rank})
        except e:
            return error("'score' must be an integer.")
    else:
        return error("You must include 'device_id', 'name', and 'score' in your request.")
