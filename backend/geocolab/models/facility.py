from ..extensions import db


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facility_type_id = db.Column(db.Integer, db.ForeignKey('facility_type.id'), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('org.id'), nullable=False)

    facility_type = db.relationship('FacilityType')
    slots = db.relationship('Slot', backref='facility')

