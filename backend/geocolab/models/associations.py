from ..extensions import db

org_manager = db.Table('org_manager',
                       db.Column('org_id', db.Integer, db.ForeignKey('org.id'), primary_key=True),
                       db.Column('manager_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                       )

facility_manager = db.Table('facility_manager',
                            db.Column('facility_id', db.Integer, db.ForeignKey('facility.id'), primary_key=True),
                            db.Column('manager_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                            )

facility_analyses = db.Table('facility_analyses',
                             db.Column('facility_id', db.Integer, db.ForeignKey('facility.id'), primary_key=True),
                             db.Column('analysis_id', db.Integer, db.ForeignKey('analysis.id'), primary_key=True)
                             )

application_analyses = db.Table('application_analyses',
                                db.Column('application_id', db.Integer, db.ForeignKey('application.id'),
                                          primary_key=True),
                                db.Column('analysis_id', db.Integer, db.ForeignKey('analysis.id'), primary_key=True)
                                )


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

    slot = db.relationship('Slot', backref='offers')
    application = db.relationship('Application', backref='offer', uselist=False)
