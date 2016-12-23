from pyticketswitch.address import Address


class TestAddress:

    def test_from_api_data(self):
        data = {
            'address_line_one': 'Metro Building',
            'address_line_two': '1 Butterwick',
            'country_code': 'uk',
            'country': 'United Kingdom',
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
        assert address.postcode == 'W6 8DL'
        assert address.country_code == 'uk'
        assert address.country == 'United Kingdom'
        assert address.email == 'lol@beans.com'
        assert address.home_phone == '020810101010101'
        assert address.work_phone == '020801010101010'
