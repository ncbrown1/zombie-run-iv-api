from flask.ext.restful import fields

player_nest_marshaller = {
    'name': fields.String
}

score_nest_marshaller = {
    'score': fields.Integer,
    'time': fields.DateTime,
}

score_marshaller = {
    'score': fields.Integer,
    'time': fields.DateTime,
    'player': fields.Nested(player_nest_marshaller)
}


player_marshaller = {
    'id': fields.Integer,
    'name': fields.String,
    'hifive_count': fields.Integer,
    'characters': fields.Integer,
    'powerup_lvl': fields.Integer,
    'scores': fields.List(fields.Nested(score_nest_marshaller))
}