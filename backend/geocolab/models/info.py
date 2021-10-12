from ..extensions import db
from ..utils import countries


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    description = db.Column(db.String())
    parent_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=True)

    children = db.relationship('Analysis', backref=db.backref('parent', remote_side=[id]))

    def __str__(self):
        def get_hierarchy(items):
            if items[0].parent is None:
                return items
            else:
                return get_hierarchy([items[0].parent] + items)

        parents = [p.name for p in get_hierarchy([self])]
        return ' > '.join(parents)


countries_enum = db.Enum(*[c[0] for c in countries], name='countries')

access_type = {
    'visit': 'Visit',
    'samples': 'Send samples',
    'any': 'Any'
}

access_type_enum = db.Enum(*access_type.keys(), name='access_type')

funding_level = {
    'none': 'None',
    'domestic': 'Domestic',
    'international': 'International'
}

funding_level_enum = db.Enum(*funding_level.keys(), name='funding_level')
