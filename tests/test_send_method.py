from pyticketswitch.send_method import SendMethod


class TestSendMethod:

    def test_from_api_data(self):
        data = {
            'send_code': 'POST',
            'send_cost': 3.5,
            'send_desc': 'Post (UK & Ireland only)',
            'send_type': 'post',
            'permitted_countries': {
                'country': [
                    {
                        'country_code': 'ie',
                        'country_desc': 'Ireland'
                    },
                    {
                        'country_code': 'uk',
                        'country_desc': 'United Kingdom'
                    }
                ]
            }
        }

        method = SendMethod.from_api_data(data)

        assert isinstance(method, SendMethod)
        assert method.code == 'POST'
        assert method.cost == 3.5
        assert method.description == 'Post (UK & Ireland only)'
        assert method.typ == 'post'
        assert len(method.permitted_countries) == 2

    def test_from_api_data_without_permitted_countries(self):
        data = {
            'send_code': 'COBO',
            'send_cost': 1.5,
            'send_desc': 'Collect from the venue',
            'send_type': 'collect',
        }

        method = SendMethod.from_api_data(data)

        assert isinstance(method, SendMethod)
        assert method.code == 'COBO'
        assert method.cost == 1.5
        assert method.description == 'Collect from the venue'
        assert method.typ == 'collect'
        assert method.permitted_countries is None
