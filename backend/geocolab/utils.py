from geonamescache import GeonamesCache


countries_cache = GeonamesCache().get_countries()
countries = [(c[0], c[1]['name']) for c in countries_cache.items()]


def init_app(app):
    @app.template_filter('country_name')
    def country_name(iso_code):
        return countries_cache.get(iso_code)['name']
