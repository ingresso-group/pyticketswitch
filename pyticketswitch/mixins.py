class PaginationMixin(object):
    """Adds pagination information to a responses meta data.

    Attributes:
        page_length (int): the number of items per page.
        page_number (int): the current page.
        pages_remaining (int): the number of pages remaining.
        results_remaining (int): the total number of remaining results after
            the current page.
        total_results (int): the total number of results.

    """

    def __init__(self, page_length=None, page_number=None, pages_remaining=None,
                 total_results=None, *args, **kwargs):
        self.page_length = page_length
        self.page_number = page_number
        self.pages_remaining = pages_remaining
        self.total_results = total_results
        super(PaginationMixin, self).__init__(*args, **kwargs)

    @classmethod
    def from_api_data(cls, data, result_key=None, *args, **kwargs):
        inst = super(PaginationMixin, cls).from_api_data(data)

        if not result_key:
            result_key = 'results'

        results = data.get(result_key, {})
        paging_data = results.get('paging_status', {})

        inst.page_length = paging_data.get('page_length')
        inst.page_number = paging_data.get('page_number')
        inst.pages_remaining = paging_data.get('pages_remaining')
        inst.results_remaining = paging_data.get('results_remaining')
        inst.total_results = paging_data.get('total_unpaged_results')

        return inst

    def is_paginated(self):
        """Indicates that the response is paginated

        Returns:
            bool: :obj:`True` when the response is omitting results due to
            pagination otherwise :obj:``False``

        """

        if not self.total_results or not self.page_length:
            return False

        if self.total_results < self.page_length:
            return False

        return True


class SeatPricingMixin(object):
    """Adds seat pricing to an object

    Attributes:
        seatprice (float): the price per seat/ticket.
        surcharge (float): additional charges per seat/ticket.
        non_offer_seatprice (float): the original price per seat/ticket when
            not on offer.
        non_offer_surcharge (float): the original additional charges per
            seat/ticket when not on offer.
    """

    def __init__(self, seatprice=None, surcharge=None, non_offer_seatprice=None,
                 non_offer_surcharge=None, *args, **kwargs):
        super(SeatPricingMixin, self).__init__(*args, **kwargs)
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.non_offer_seatprice = non_offer_seatprice
        self.non_offer_surcharge = non_offer_surcharge

    @staticmethod
    def kwargs_from_api_data(data):
        kwargs = {
            'seatprice': data.get('sale_seatprice'),
            'surcharge': data.get('sale_surcharge'),
            'non_offer_seatprice': data.get('non_offer_sale_seatprice'),
            'non_offer_surcharge': data.get('non_offer_sale_surcharge'),
        }
        return kwargs

    def combined_price(self):
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
        assert self.seatprice is not None, 'seatprice data missing'
        assert self.surcharge is not None, 'surcharge data missing'
        return self.seatprice + self.surcharge

    def non_offer_combined_price(self):
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
        assert self.non_offer_seatprice is not None, 'non_offer_seatprice data missing'
        assert self.non_offer_surcharge is not None, 'non_offer_surcharge data missing'
        return self.non_offer_seatprice + self.non_offer_surcharge
