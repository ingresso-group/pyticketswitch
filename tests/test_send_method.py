from decimal import Decimal
from pyticketswitch.send_method import SendMethod


class TestSendMethod:

    def test_from_api_data(self):
        data = {
            'send_code': 'POST',
            'send_cost': 3.5,
            'send_desc': 'Post (UK & Ireland only)',
            'send_type': 'post',
            'send_final_comment': 'allow some time',
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
            },
            'send_cost_tax_component': 0.95,
            'trans_fee_component': 1.5
        }

        method = SendMethod.from_api_data(data)

        assert isinstance(method, SendMethod)
        assert method.code == 'POST'
        assert method.cost == 3.5
        assert method.description == 'Post (UK & Ireland only)'
        assert method.type == 'post'
        assert method.final_comment == 'allow some time'
        assert len(method.permitted_countries) == 2
        assert method.send_cost_tax_component == 0.95
        assert method.trans_fee_component == 1.5

    def test_from_api_data_with_decimal(self):
        data = {
            'send_code': 'POST',
            'send_cost': Decimal('3.5'),
            'send_desc': 'Post (UK & Ireland only)',
            'send_type': 'post',
            'send_final_comment': 'allow some time',
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
            },
            'send_cost_tax_component': Decimal('0.95'),
            'trans_fee_component': Decimal('1.5')
        }

        method = SendMethod.from_api_data(data)

        assert isinstance(method, SendMethod)
        assert method.code == 'POST'
        assert method.cost == Decimal('3.5')
        assert method.description == 'Post (UK & Ireland only)'
        assert method.type == 'post'
        assert method.final_comment == 'allow some time'
        assert len(method.permitted_countries) == 2
        assert method.send_cost_tax_component == Decimal('0.95')
        assert method.trans_fee_component == Decimal('1.5')

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
        assert method.type == 'collect'
        assert method.permitted_countries is None
