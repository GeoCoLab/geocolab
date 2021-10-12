from datetime import datetime as dt

from .info import countries_enum, access_type_enum, funding_level_enum
from ..extensions import db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    about_request = db.Column(db.String)
    about_you = db.Column(db.String)
    restrictions = db.Column(db.String)
    desired_location = db.Column(countries_enum)
    current_org = db.Column(db.String(200))
    additional_requirements = db.Column(db.String)
    date_from = db.Column(db.Date, nullable=False, default=dt.now().date())
    date_to = db.Column(db.Date)
    days_estimate = db.Column(db.Integer)
    samples_estimate = db.Column(db.Integer)
    date_submitted = db.Column(db.Date)
    is_submitted = db.Column(db.Boolean, default=False, nullable=False)
    access_type = db.Column(access_type_enum, default='any', nullable=False)
    funding_level = db.Column(funding_level_enum, default='none', nullable=False)
    prep_required = db.Column(db.Boolean, default=True, nullable=False)
    other_analyses = db.Column(db.String)

    analyses = db.relationship('Analysis', secondary='application_analyses', lazy=True)

    @property
    def funding_required(self):
        return self.funding_level != 'international'
