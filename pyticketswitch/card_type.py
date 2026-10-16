from __future__ import annotations

from pyticketswitch.mixins import JSONMixin


class CardType(JSONMixin):
    """Type of card that will be accepted during the payment process

    Attributes:
        code (str): identifier for the card type.
        description (str): human readable description of the card type.

    """

    def __init__(self, code: str | None = None, description: str | None = None) -> None:
        self.code = code
        self.description = description

    def __repr__(self) -> str:
        return f"<CardType {self.code}: {self.description}>"
