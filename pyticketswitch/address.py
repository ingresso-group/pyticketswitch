class Address(object):

    def __init__(self, lines=None, country_code=None, county=None,
                 email=None, home_phone=None, postcode=None, town=None,
                 work_phone=None):

        self.lines = lines
        self.country_code = country_code
        self.county = county
        self.email = email
        self.home_phone = home_phone
        self.postcode = postcode
        self.town = town
        self.work_phone = work_phone

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'country_code': data.get('country_code'),
            'county': data.get('county'),
            'email': data.get('email_address'),
            'home_phone': data.get('home_phone'),
            'postcode': data.get('postcode'),
            'town': data.get('town'),
            'work_phone': data.get('work_phone'),
            'lines': [
                data.get('address_line_one'),
                data.get('address_line_two'),
            ]
        }

        return cls(**kwargs)
