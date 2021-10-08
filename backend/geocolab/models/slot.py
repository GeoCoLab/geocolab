from ..extensions import db
from datetime import datetime as dt


class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_open = db.Column(db.Boolean)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)

    @property
    def current_offer(self):
        # this is not the best, but it'll do for now
        today = dt.now().date()
        try:
            return next(m for m in self.offers if m.date_from <= today <= m.date_to)
        except StopIteration:
            return None

