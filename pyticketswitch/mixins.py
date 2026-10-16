from __future__ import annotations

import datetime
import decimal
import json
from typing import TYPE_CHECKING, Any, cast

from pyticketswitch import utils

if TYPE_CHECKING:
    from pyticketswitch._typing import Number


class JSONMixin:
    """Adds json encoding functionality to objects."""

    def __jsondict__(
        self, hide_none: bool = True, hide_empty: bool = True
    ) -> dict[str, Any]:

        def sanitise(obj: Any) -> Any:
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()

            if isinstance(obj, datetime.date):
                return obj.isoformat()

            if isinstance(obj, decimal.Decimal):
                return float(obj)

            if hasattr(obj, "__jsondict__"):
                return obj.__jsondict__(hide_none=hide_none, hide_empty=hide_empty)

            if isinstance(obj, list):
                return [sanitise(item) for item in obj]

            if isinstance(obj, dict):
                return {key: sanitise(value) for key, value in obj.items()}

            return obj

        return {
            key: sanitise(obj)
            for key, obj in self.__dict__.items()
            # when hiding None's and the object is None, skip the object
            if not (hide_none and obj is None)
            # when hiding empty iterators and the object is an iterator and
            # it's empty, skip the object.
            if not (hide_empty and hasattr(obj, "__iter__") and not obj)
        }

    def as_dict_for_json(
        self, hide_none: bool = True, hide_empty: bool = True
    ) -> dict[str, Any]:
        """Generate a json serialisable dictionary from the object

        Dates are changed to strings in ISO 8601 format.

        Lists children are recursively serialised.

        Dictionary values are recursively serialised, keys are left as is.

        Objects that implement __jsondict__ return the result of calling
        __jsondict__ on the object.

        Args:
            hide_none (bool, optional): when :obj:`True` the returned
                dictionary will not include attributes who's value is
                :obj:`None`.
            hide_empty (bool, optional): when :obj:`True` the returned
                dictionary will not include attributes who's value is iterable
                and has a length of zero.

        Returns:
            dict: a dictionary representation of the object.

        """
        return self.__jsondict__(hide_none=hide_none, hide_empty=hide_empty)

    def as_json(
        self, hide_none: bool = True, hide_empty: bool = True, **kwargs: Any
    ) -> str:
        """Generate a json represetation of an object.

        Args:
            hide_none (bool): when :obj:`True` the returned
                dictionary will not include attributes who's value is
                :obj:`None`.
            hide_empty (bool): when :obj:`True` the returned
                dictionary will not include attributes who's value is iterable
                and has a length of zero.
            **kwargs: passed to :py:func:`json.dumps`.

        Returns:
            str: a json representation of an object

        """

        return json.dumps(
            self.as_dict_for_json(hide_none=hide_none, hide_empty=hide_empty), **kwargs
        )


class PaginationMixin:
    """Adds pagination information to a responses meta data.

    Attributes:
        page_length (int): the number of items per page.
        page_number (int): the current page.
        pages_remaining (int): the number of pages remaining.
        results_remaining (int): the total number of remaining results after
            the current page.
        total_results (int): the total number of results.

    """

    def __init__(
        self,
        page_length: int | None = None,
        page_number: int | None = None,
        pages_remaining: int | None = None,
        total_results: int | None = None,
        results_remaining: int | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.page_length = page_length
        self.page_number = page_number
        self.pages_remaining = pages_remaining
        self.results_remaining = results_remaining
        self.total_results = total_results
        super().__init__(*args, **kwargs)

    @classmethod
    def from_api_data(
        cls,
        data: dict[str, Any],
        result_key: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        # cooperative mixin: from_api_data is provided by the next class in the
        # MRO, so the concrete return type is not known here
        inst = cast("Any", super()).from_api_data(data)

        if not result_key:
            result_key = "results"

        results = data.get(result_key, {})
        paging_data = results.get("paging_status", {})

        inst.page_length = paging_data.get("page_length")
        inst.page_number = paging_data.get("page_number")
        inst.pages_remaining = paging_data.get("pages_remaining")
        inst.results_remaining = paging_data.get("results_remaining")
        inst.total_results = paging_data.get("total_unpaged_results")

        return inst

    def is_paginated(self) -> bool:
        """Indicates that the response is paginated

        Returns:
            bool: :obj:`True` when the response is omitting results due to
            pagination otherwise :obj:``False``

        """

        if not self.total_results or not self.page_length:
            return False

        return not self.total_results < self.page_length


class SeatPricingMixin:
    """Adds seat pricing to an object

    Attributes:
        seatprice (float): the price per seat/ticket.
        surcharge (float): additional charges per seat/ticket.
        non_offer_seatprice (float): the original price per seat/ticket when
            not on offer.
        non_offer_surcharge (float): the original additional charges per
            seat/ticket when not on offer.
    """

    def __init__(
        self,
        seatprice: Number | None = None,
        surcharge: Number | None = None,
        non_offer_seatprice: Number | None = None,
        non_offer_surcharge: Number | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.non_offer_seatprice = non_offer_seatprice
        self.non_offer_surcharge = non_offer_surcharge

    @staticmethod
    def kwargs_from_api_data(data: dict[str, Any]) -> dict[str, Any]:
        return {
            "seatprice": data.get("sale_seatprice"),
            "surcharge": data.get("sale_surcharge"),
            "non_offer_seatprice": data.get("non_offer_sale_seatprice"),
            "non_offer_surcharge": data.get("non_offer_sale_surcharge"),
        }

    def combined_price(self) -> Number:
        """Returns the combined seatprice and surcharge.

        This method assumes that we have both a seatprice and surcharge.
        In the situation where are missing either a seatprice or a surcharge
        then we don't have all the information to be able provide this
        information.

        Returns:
            float: the combined seatprice and surcharge

        Raises:
            AssertionError: It might seem like the obvious thing to do would be
                to assume the missing data was in fact zero and simply allow the
                addition to continue. However that would be somewhat dangerous when
                we are talking about prices, and it's better to actually raise an
                exception to indicate that there was a problem with the objects
                data, than to inform a customer that the tickets are free or have
                no booking fees

        """
        if self.seatprice is None:
            raise AssertionError("seatprice data missing")
        if self.surcharge is None:
            raise AssertionError("surcharge data missing")

        return utils.add_prices(self.seatprice, self.surcharge)

    def non_offer_combined_price(self) -> Number:
        """Returns the combined non offer seatprice and surcharge.

        This method assumes that we have both a seatprice and surcharge.
        In the situation where are missing either a seatprice or a surcharge
        then we don't have all the information to be able provide this
        information.

        Returns:
            float: the combined seatprice and surcharge

        Raises:
            AssertionError: It might seem like the obvious thing to do would be
                to assume the missing data was in fact zero and simply allow the
                addition to continue. However that would be somewhat dangerous when
                we are talking about prices, and it's better to actually raise an
                exception to indicate that there was a problem with the objects
                data, than to inform a customer that the tickets are free or have
                no booking fees

        """
        if self.non_offer_seatprice is None:
            raise AssertionError("non_offer_seatprice data missing")
        if self.non_offer_surcharge is None:
            raise AssertionError("non_offer_surcharge data missing")
        return utils.add_prices(self.non_offer_seatprice, self.non_offer_surcharge)
