from geonamescache import GeonamesCache


countries = list(GeonamesCache().get_countries().values())
