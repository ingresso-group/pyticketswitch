from pyticketswitch.customer import Customer


class TestCustomer:

    def test_from_api_data(self):

        data = {
            "addr_line_one": "Metro Building",
            "addr_line_one_latin": "METRO BUILDING",
            "addr_line_two": "1 Butterwick",
            "addr_line_two_latin": "1 BUTTERWICK",
            "agent_ref": "foobar123",
            "country": "United Kingdom",
            "country_code": "uk",
            "country_latin": "UNITED KINGDOM",
            "county": "London",
            "county_latin": "LONDON",
            "dp_supplier": True,
            "dp_user": True,
            "dp_world": True,
            "email_addr": "tester@gmail.com",
            "first_name": "Test",
            "first_name_latin": "TEST",
            "home_phone": "0203 137 7420",
            "work_phone": "079888888888",
            "phone": "079000000000",
            "initials": "l.o.l",
            "initials_latin": "L.O.L",
            "last_name": "Tester",
            "last_name_latin": "TESTER",
            "postcode": "w6 8dl",
            "postcode_latin": "W6 8DL",
            "suffix": "esq",
            "suffix_latin": "ESQ",
            "title": "rt.hon",
            "title_latin": "RT.HON",
            "town": "Hammersmith",
            "town_latin": "HAMMERSMITH",
        }

        customer = Customer.from_api_data(data)

        assert customer.first_name == 'Test'
        assert customer.first_name_latin == 'TEST'

        assert customer.last_name == 'Tester'
        assert customer.last_name_latin == 'TESTER'

        assert customer.address_lines == [
            'Metro Building',
            '1 Butterwick',
        ]

        assert customer.address_lines_latin == [
            'METRO BUILDING',
            '1 BUTTERWICK',
        ]

        assert customer.country_code == 'uk'

        assert customer.title == 'rt.hon'
        assert customer.title_latin == 'RT.HON'

        assert customer.initials == 'l.o.l'
        assert customer.initials_latin == 'L.O.L'

        assert customer.suffix == 'esq'
        assert customer.suffix_latin == 'ESQ'

        assert customer.email == 'tester@gmail.com'

        assert customer.post_code == 'w6 8dl'
        assert customer.post_code_latin == 'W6 8DL'

        assert customer.town == 'Hammersmith'
        assert customer.town_latin == 'HAMMERSMITH'

        assert customer.county == 'London'
        assert customer.county_latin == 'LONDON'

        assert customer.country == 'United Kingdom'
        assert customer.country_latin == 'UNITED KINGDOM'

        assert customer.phone == '079000000000'
        assert customer.home_phone == '0203 137 7420'
        assert customer.work_phone == '079888888888'

        assert customer.agent_reference == 'foobar123'

        assert customer.supplier_can_use_data is True
        assert customer.user_can_use_data is True
        assert customer.world_can_use_data is True

    def test_as_api_parameters(self):
        customer = Customer(
            first_name='Test',
            first_name_latin='TEST',
            last_name='Tester',
            last_name_latin='TESTER',
            address_lines=['Metro Building', '1 Butterwick'],
            address_lines_latin=['METRO BUILDING', '1 BUTTERWICK'],
            country_code='uk',
            title='rt.hon',
            title_latin='RT.HON',
            initials='l.o.l',
            initials_latin='L.O.L',
            suffix='esq',
            suffix_latin='ESQ',
            email='tester@gmail.com',
            post_code='w6 8dl',
            post_code_latin='W6 8DL',
            town='Hammersmith',
            town_latin='HAMMERSMITH',
            county='London',
            county_latin='LONDON',
            country='United Kingdom',
            country_latin='UNITED KINGDOM',
            phone='079000000000',
            home_phone='0203 137 7420',
            work_phone='079888888888',
            agent_reference='foobar123',
            supplier_can_use_data=True,
            user_can_use_data=True,
            world_can_use_data=True,
        )

        assert customer.as_api_parameters() == {
            'first_name': 'Test',
            'last_name': 'Tester',
            'address_line_one': 'Metro Building',
            'address_line_two': '1 Butterwick',
            'country_code': 'uk',
            'title': 'rt.hon',
            'initials': 'l.o.l',
            'suffix': 'esq',
            'email_address': 'tester@gmail.com',
            'postcode': 'w6 8dl',
            'town': 'Hammersmith',
            'county': 'London',
            'phone': '079000000000',
            'home_phone': '0203 137 7420',
            'work_phone': '079888888888',
            'agent_ref': 'foobar123',
            'supplier_can_use_customer_data': True,
            'user_can_use_customer_data': True,
            'world_can_use_customer_data': True,
        }
