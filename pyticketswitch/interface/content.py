class Content(object):

    def __init__(self, name=None, value=None, value_html=None):

        self.name = name
        self.value = value
        self.value_html = value_html

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'name': data.get('name', None),
            'value': data.get('value', None),
            'value_html': data.get('value_html', None),
        }

        return cls(**kwargs)
