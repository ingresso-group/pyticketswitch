from pyticketswitch.country import Country


class TestCountry:

    def test_from_api_data(self):
        data = {
            'country_code': 'uk',
            'country_desc': 'United Kingdom'
        }

        country = Country.from_api_data(data)

        assert country.code == 'uk'
        assert country.description == 'United Kingdom'

    def test_repr(self):

        country = Country('uk', description='United Kingdom')
        assert repr(country) == '<Country uk:United Kingdom>'
