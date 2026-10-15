from pyticketswitch.country import Country


class TestCountry:
    def test_from_api_data(self):
        data = {"country_code": "uk", "country_desc": "United Kingdom"}

        country = Country.from_api_data(data)

        assert country.code == "uk"
        assert country.description == "United Kingdom"

    def test_repr_without_description(self):
        assert repr(Country("uk", description=None)) == "<Country uk:None>"

    def test_repr_with_description(self):
        assert repr(Country("uk", description="United Kingdom")) == (
            "<Country uk:'United Kingdom'>"
        )
