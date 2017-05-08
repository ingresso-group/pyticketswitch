from pyticketswitch.mixins import JSONMixin


class CardType(JSONMixin, object):
    """Type of card that will be accepted during the payment process

    Attributes:
        code (str): identifier for the card type.
        description (str): human readable description of the card type.

    """

    def __init__(self, code=None, description=None):
        self.code = code
        self.description = description

    def __repr__(self):
        return u'<CardType {}: {}>'.format(self.code, self.description)
