from flask_login import current_user

from .info import countries_enum, funding_level_enum, access_type_enum
from ..extensions import db


class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    country = db.Column(countries_enum)
    ror_id = db.Column(db.String(9), index=True)
    funding_limit = db.Column(db.Integer, default=0)
    funding_level = db.Column(funding_level_enum, default='none', nullable=False)
    accepted_access_types = db.Column(access_type_enum, default='any', nullable=False)

    facilities = db.relationship('Facility', backref='org')

    @property
    def can_edit(self):
        if not current_user.is_authenticated:
            return False
        elif current_user.is_admin:
            return True
        else:
            return current_user.id in [u.id for u in self.managers]

    @property
    def will_fund(self):
        return self.funding_level != 'none'
