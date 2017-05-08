from pyticketswitch.address import Address


class TestAddress:

    def test_from_api_data(self):
        data = {
            'address_line_one': 'Metro Building',
            'address_line_two': '1 Butterwick',
            'country_code': 'uk',
            'county': 'London',
            'email_address': 'lol@beans.com',
            'home_phone': '020810101010101',
            'postcode': 'W6 8DL',
            'town': 'Hammersmith, London',
            'work_phone': '020801010101010'
        }

        address = Address.from_api_data(data)

        assert address.lines[0] == 'Metro Building'
        assert address.lines[1] == '1 Butterwick'
        assert address.town == 'Hammersmith, London'
        assert address.post_code == 'W6 8DL'
        assert address.country_code == 'uk'
        assert address.county == 'London'
        assert address.email == 'lol@beans.com'
        assert address.home_phone == '020810101010101'
        assert address.work_phone == '020801010101010'

    def test_as_api_billing_address_parameters(self):

        address = Address(
            lines=['1303 Boulder Lane', 'Landslide district'],
            country_code='us',
            county='Louisana',
            town='Bedrock',
            post_code='70777',
        )

        params = address.as_api_billing_address_parameters()

        assert params == {
            'billing_address_line_one': '1303 Boulder Lane',
            'billing_address_line_two': 'Landslide district',
            'billing_country_code': 'us',
            'billing_county': 'Louisana',
            'billing_town': 'Bedrock',
            'billing_postcode': '70777',
        }

    def test_as_api_billing_address_parameters_single(self):

        address = Address(
            lines=['1303 Boulder Lane'],
            country_code='us',
            county='Louisana',
            town='Bedrock',
            post_code='70777',
        )

        params = address.as_api_billing_address_parameters()

        assert params == {
            'billing_address_line_one': '1303 Boulder Lane',
            'billing_country_code': 'us',
            'billing_county': 'Louisana',
            'billing_town': 'Bedrock',
            'billing_postcode': '70777',
        }
