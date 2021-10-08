from .info import countries_enum
from ..extensions import db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason_for_request = db.Column(db.String)
    restrictions = db.Column(db.String)
    current_location = db.Column(countries_enum)
    current_org = db.Column(db.String(200))
    additional_requirements = db.Column(db.String)
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)
    date_submitted = db.Column(db.Date)
    is_submitted = db.Column(db.Boolean)

    analyses = db.relationship('Analysis', secondary='application_analyses', lazy=True)
