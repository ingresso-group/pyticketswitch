from pyticketswitch.user import User


class TestUser:

    def test_from_api_data(self):

        data = {
            'backend_group': 'demo_internal_credit_group',
            'content_group': 'demo_content_group',
            'default_country_code': 'uk',
            'is_b2b': True,
            'real_name': 'Demonstration User',
            'statement_descriptor': 'TICKETSWITCH-USER',
            'style': 'fixed-tabs',
            'sub_style': 'styled-aff-default',
            'sub_sub_style': 'ingresso-generic',
            'sub_user': 'pyticketswitch-test',
            'user_id': 'demo'
        }

        user = User.from_api_data(data)

        assert user.id == 'demo'
        assert user.name == 'Demonstration User'
        assert user.country == 'uk'
        assert user.sub_user == 'pyticketswitch-test'
        assert user.is_b2b is True
        assert user.statement_descriptor == 'TICKETSWITCH-USER'
        assert user.backend_group == 'demo_internal_credit_group'
        assert user.content_group == 'demo_content_group'
