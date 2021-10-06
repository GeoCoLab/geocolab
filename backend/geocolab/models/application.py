from ..extensions import db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    facility_type_id = db.Column(db.Integer, db.ForeignKey('facility_type.id'), nullable=False)

    facility_type = db.relationship('FacilityType')
