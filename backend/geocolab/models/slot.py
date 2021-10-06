from ..extensions import db


class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
