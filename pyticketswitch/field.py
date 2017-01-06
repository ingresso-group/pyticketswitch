class Field(object):

    def __init__(self, name, label, data):
        self.name = name
        self.label = label
        self.data = data

    @classmethod
    def from_api_data(cls, data):
        kwargs = {
            'name': data.get('custom_field_name'),
            'label': data.get('custom_field_label'),
            'data': data.get('custom_field_data'),
        }

        return cls(**kwargs)
