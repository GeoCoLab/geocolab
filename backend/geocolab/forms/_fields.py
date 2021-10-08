from flask_login import current_user
from wtforms import SelectField, SelectMultipleField
from flask_wtf import FlaskForm

from ..models import Analysis
from ..utils import countries


class CountryField(SelectField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = sorted(countries, key=lambda x: x[1])
        super(CountryField, self).__init__(*args, **kwargs)


class AnalysisField(SelectMultipleField):
    def __init__(self, *args, **kwargs):
        kwargs['coerce'] = int
        kwargs['choices'] = [(a.id, str(a)) for a in Analysis.query.all() if len(a.children) == 0]
        super(AnalysisField, self).__init__(*args, **kwargs)

    def process_data(self, value):
        super(AnalysisField, self).process_data([v.id for v in value] if value else value)


class OrgField(SelectField):
    def __init__(self, *args, **kwargs):
        if current_user.is_authenticated:
            kwargs['choices'] = [(f.id, f.name) for f in current_user.managed_orgs]
        else:
            kwargs['choices'] = []
        super(OrgField, self).__init__(*args, **kwargs)

    @property
    def predefined(self):
        return self.object_data is not None

    @property
    def text(self):
        return dict(self.choices)[int(self.data)]
