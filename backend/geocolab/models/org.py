from ..extensions import db
from flask_login import current_user
from ..utils import countries


class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    country = db.Column(db.Enum(*[c[0] for c in countries], name='countries'))
    ror_id = db.Column(db.String(9), index=True, unique=True)

    facilities = db.relationship('Facility', backref='org')

    @property
    def can_edit(self):
        if not current_user.is_authenticated:
            return False
        elif current_user.is_admin:
            return True
        else:
            return current_user.id in [u.id for u in self.managers]
