from flask_login import current_user

from .info import countries_enum
from ..extensions import db


class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    country = db.Column(countries_enum)
    ror_id = db.Column(db.String(9), index=True)
    will_fund_travel = db.Column(db.Boolean, default=True)

    facilities = db.relationship('Facility', backref='org')

    @property
    def can_edit(self):
        if not current_user.is_authenticated:
            return False
        elif current_user.is_admin:
            return True
        else:
            return current_user.id in [u.id for u in self.managers]
