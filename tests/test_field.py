from pyticketswitch.field import Field


class TestField:

    def test_from_api_data(self):

        data = {
            'custom_field_name': 'foo_bar',
            'custom_field_label': 'Foo Bar',
            'custom_field_data': 'this is a foo and a bar',
        }

        field = Field.from_api_data(data)
        assert field.name == 'foo_bar'
        assert field.label == 'Foo Bar'
        assert field.data == 'this is a foo and a bar'
