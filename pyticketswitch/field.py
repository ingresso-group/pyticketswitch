from pyticketswitch.mixins import JSONMixin


class Field(JSONMixin, object):
    """Describes a custom field for an event

    Attributes:
        name (str): the name of the field.
        label (str): human readble name of the field.
        data (str): the field data.

    """

    def __init__(self, name, label, data):
        self.name = name
        self.label = label
        self.data = data

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Field object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a field.

        Returns:
            :class:`Field <pyticketswitch.field.Field>`: a new
            :class:`Field <pyticketswitch.field.Field>` object
            populated with the data from the api.

        """

        kwargs = {
            'name': data.get('custom_field_name'),
            'label': data.get('custom_field_label'),
            'data': data.get('custom_field_data'),
        }

        return cls(**kwargs)
