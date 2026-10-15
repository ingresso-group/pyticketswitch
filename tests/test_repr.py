import pytest

from pyticketswitch.discount import Discount
from pyticketswitch.event import Event
from pyticketswitch.price_band import PriceBand
from pyticketswitch.send_method import SendMethod
from pyticketswitch.ticket_type import TicketType


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        (SendMethod("POST", description="Post"), "<SendMethod POST:'Post'>"),
        (SendMethod("POST", description=None), "<SendMethod POST:None>"),
        (Discount("ADULT", description="Adult"), "<Discount ADULT:'Adult'>"),
        (Discount("ADULT", description=None), "<Discount ADULT:None>"),
        (Event("6IF", description="Show"), "<Event 6IF:'Show'>"),
        (Event("6IF", description=None), "<Event 6IF:None>"),
        (TicketType("STALLS", description="Stalls"), "<TicketType STALLS: 'Stalls'>"),
        (TicketType("STALLS", description=None), "<TicketType STALLS: None>"),
        (
            PriceBand("A", default_discount=None, description="Top"),
            "<PriceBand A:'Top'>",
        ),
        (PriceBand("A", default_discount=None, description=None), "<PriceBand A>"),
    ],
)
def test_repr_shows_description(obj, expected):
    assert repr(obj) == expected
