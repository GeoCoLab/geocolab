from flask_login import UserMixin
from sqlalchemy.sql import func

from .info import countries_enum
from ..extensions import db, crypt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime(), server_default=func.now())
    country = db.Column(countries_enum)
    role = db.Column(db.Enum('user', 'admin', name='roles'), server_default='user')

    managed_orgs = db.relationship('Org', secondary='org_manager', backref=db.backref('managers', lazy=True), lazy=True)
    _facilities = db.relationship('Facility', secondary='facility_manager',
                                  backref=db.backref('_managers', lazy=True), lazy=True)
    applications = db.relationship('Application', backref='user', lazy=True)

    def password_set(self, plaintext):
        self.password = crypt.hash(plaintext)

    def password_verify(self, plaintext):
        return crypt.verify(plaintext, self.password)

    @property
    def managed_facilities(self):
        facilities = [f for f in self._facilities]
        for org in self.managed_orgs:
            facilities += org.facilities
        return facilities

    @property
    def is_org_manager(self):
        return len(self.managed_orgs) > 0

    @property
    def is_facility_manager(self):
        return len(self.managed_facilities) > 0

    @property
    def has_pending_applications(self):
        return len(self.applications) > 0

    @property
    def is_admin(self):
        return self.role == 'admin'
