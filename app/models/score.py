from .. import db
from player import Player
from datetime import datetime

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    score = db.Column(db.Integer, index=True)
    time = db.Column(db.DateTime)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))

    player = db.relationship('Player', backref='scores')

    def __init__(self, score, name, device_id):
        player = Player.query.filter_by(device_id=device_id).filter_by(name=name).first()
        if player is None:
            player = Player(device_id, name)
            player.save()

        self.score = score
        self.time = datetime.now()
        self.player = player
        player.scores.append(self)
        player.save()

    def save(self):
        """
        Operation: model.save()
        Preconditions:
            - Model has been properly created and instantiated
        Postconditions:
            - Database contains a row with new model contents
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return 'Score {}>'.format(self.id)
