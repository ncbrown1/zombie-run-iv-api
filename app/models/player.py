from .. import db

class Player(db.Model):
    __tablename__= 'players'

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    device_id = db.Column(db.String, index=True)
    name = db.Column(db.String(10), index=True)
    hifive_count = db.Column(db.Integer)
    characters = db.Column(db.Integer)
    powerup_lvl = db.Column(db.Integer)

    # scores = db.relationship('Score', backref='player', lazy='dynamic')

    def __init__(self, device_id, name, hifive_count=0, characters=1, powerup_lvl=1):
        self.device_id = device_id
        self.name = name
        self.hifive_count = hifive_count
        self.characters = characters
        self.powerup_lvl = powerup_lvl

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return 'Player {}>'.format(self.id)
