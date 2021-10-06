from ..extensions import db


class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    country = db.Column(db.String(3))
    ror_id = db.Column(db.String(9))

    facilities = db.relationship('Facility', backref='org')
