from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyticketswitch.country import Country
from pyticketswitch.mixins import JSONMixin

if TYPE_CHECKING:
    from pyticketswitch._typing import Number


class SendMethod(JSONMixin):
    """Describes a method of sending tickets to a customer.

    Attributes:
        code (str): identifier for the send method.
        cost (float): additional cost to the customer for this send method.
        description (str): human readable description of the send method.
        type (str): indicates the type of the send method.
        can_generate_self_print (bool): indicates if the send method can
            self print a voucher
        self_print_voucher_url (str): url for the client to download their
            voucher from
        final_comment (str): comment about dispatching tickets
        send_cost_tax_component (float): tax of the send cost
        trans_fee_component (float): transaction fee added by repricing rule.
    """

    def __init__(
        self,
        code: str | None,
        cost: Number | None = None,
        description: str | None = None,
        typ: str | None = None,
        permitted_countries: list[Country] | None = None,
        can_generate_self_print: bool | None = False,
        self_print_voucher_url: str | None = None,
        final_comment: str | None = None,
        send_cost_tax_component: Number | None = None,
        trans_fee_component: Number | None = None,
    ) -> None:
        self.code = code
        self.cost = cost
        self.description = description
        self.type = typ
        self.permitted_countries = permitted_countries
        self.can_generate_self_print = can_generate_self_print
        self.self_print_voucher_url = self_print_voucher_url
        self.final_comment = final_comment
        self.send_cost_tax_component = send_cost_tax_component
        self.trans_fee_component = trans_fee_component

    @classmethod
    def from_api_data(cls, data: dict[str, Any]) -> SendMethod:
        """Creates a new SendMethod object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a send method.

        Returns:
            :class:`SendMethod <pyticketswitch.send_method.SendMethod>`: a new
            :class:`SendMethod <pyticketswitch.send_method.SendMethod>` object
            populated with the data from the api.

        """
        kwargs = {
            "code": data.get("send_code"),
            "description": data.get("send_desc"),
            "typ": data.get("send_type"),
            "can_generate_self_print": data.get("can_generate_self_print"),
            "self_print_voucher_url": data.get("self_print_voucher_url"),
            "final_comment": data.get("send_final_comment"),
        }

        cost = data.get("send_cost", 0.0)
        kwargs.update(cost=cost)

        trans_fee_component = data.get("trans_fee_component", 0.0)
        kwargs.update(trans_fee_component=trans_fee_component)

        permitted_countries_raw = data.get("permitted_countries", {})

        if permitted_countries_raw:
            permitted_countries_raw = permitted_countries_raw.get("country", [])

            permitted_countries = [
                Country.from_api_data(country) for country in permitted_countries_raw
            ]

            kwargs.update(permitted_countries=permitted_countries)

        send_cost_tax_component = data.get("send_cost_tax_component")
        if send_cost_tax_component is not None:
            kwargs.update(send_cost_tax_component=send_cost_tax_component)

        return cls(**kwargs)

    def __repr__(self) -> str:
        return f"<SendMethod {self.code}:{self.description!r}>"
