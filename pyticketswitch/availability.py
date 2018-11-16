import datetime
from pyticketswitch.mixins import JSONMixin
from pyticketswitch.currency import CurrencyMeta
from pyticketswitch.misc import MONTH_NUMBERS


class AvailabilityMeta(CurrencyMeta):
    """Meta data about an availability response

    Attributes:
        contiguous_seat_selection_only (bool): indicates that the backend
            system will only allow seats to be selected that are in a
            contiguous line.
        valid_quantities (list): list of valid number of tickets available for
            selection.
        max_bundle_size (int): maximum bundle size for this event. If it is
            `None` then there is no maximum size.
        currencies (dict): dictionary of
            :class:`Currency <pytickectswitch.currency.Currency>`) objects
            indexed on currency code.
        default_currency_code (str): unless other wise specified all prices in
            the related response will be in this currency.
        desired_currency_code (str):
            the currency that the user account is expecting. Useful for
            conversions.
        backend_is_broken (bool): indicates that the backend system is presently
            marked as broken.
        backend_is_down (bool): indicates that we are not currently able to
            contact the backend system.
        backend_throttle_failed (bool): indicates that your call was throttled
            and failed to get a slot inside a viable timeframe. When true this
            indicates that the backend system is under heavy load.

    """
    def __init__(self, contiguous_seat_selection_only=True, currency=None,
                 valid_quantities=None, max_bundle_size=None, backend_is_down=False,
                 backend_is_broken=False, backend_throttle_failed=False,
                 *args, **kwargs):
        self.contiguous_seat_selection_only = contiguous_seat_selection_only
        self.currency = currency
        self.max_bundle_size = max_bundle_size
        self.valid_quantities = valid_quantities
        self.backend_is_broken = backend_is_broken
        self.backend_is_down = backend_is_down
        self.backend_throttle_failed = backend_throttle_failed
        super(AvailabilityMeta, self).__init__(*args, **kwargs)

    @classmethod
    def from_api_data(cls, data):
        """Creates a new AvailabilityMeta object from API data from ticketswitch.

        Args:
            data (dict): the whole response from the availability call.

        Returns:
            :class:`AvailabilityMeta <pyticketswitch.availability.AvailabilityMeta>`:
            a new
            :class:`AvailabilityMeta <pyticketswitch.availability.AvailabilityMeta>`
            object populated with the data from the api.

        """
        inst = super(AvailabilityMeta, cls).from_api_data(data)

        inst.valid_quantities = data.get('valid_quantities')
        inst.max_bundle_size = data.get('max_bundle_size')
        inst.contiguous_seat_selection_only = data.get('contiguous_seat_selection_only', True)
        inst.backend_is_broken = data.get('backend_is_broken')
        inst.backend_is_down = data.get('backend_is_down')
        inst.backend_throttle_failed = data.get('backend_throttle_failed')

        return inst


class AvailabilityDetails(JSONMixin, object):
    """Details about the available tickets of a performance.

    Attributes:
        ticket_type_code (str): identifier of the ticket type.
        ticket_type_description (str): human readable description of the ticket
            type.
        price_band_code (str): identifier of the price band.
        price_band_description (str): human readable description of the price
            band.
        seatprice (float): price of an individual seat.
        surcharge (float): additional charges per seat.
        full_seatprice (float): the non-offer price of an individual seat.
        full_surcharge (float): the non-offer additional charges per seat.
        currency (str): the currency of the prices.
        first_date (datetime.datetime): the first date and time this
            combination of ticket type and price band is available from.
        last_date (datetime.datetime): the latest date and time this
            combination of ticket type and price band is available from.
        valid_quantities (list): list of valid number of tickets available for
            selection.
        cached_number_available (int): the maximum number of consecutive
            tickets available.

    """

    def __init__(self, ticket_type=None, price_band=None,
                 ticket_type_description=None, price_band_description=None,
                 seatprice=None, surcharge=None, full_seatprice=None,
                 full_surcharge=None, currency=None, first_date=None,
                 percentage_saving=None, absolute_saving=None,
                 last_date=None, calendar_masks=None,
                 weekday_mask=None, valid_quantities=None,
                 cached_number_available=None):

        self.ticket_type = ticket_type
        self.ticket_type_description = ticket_type_description
        self.price_band = price_band
        self.price_band_description = price_band_description
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.full_seatprice = full_seatprice
        self.full_surcharge = full_surcharge
        self.percentage_saving = percentage_saving
        self.absolute_saving = absolute_saving
        self.currency = currency
        self.first_date = first_date
        self.last_date = last_date
        self._calendar_masks = calendar_masks
        self._weekday_mask = weekday_mask
        self.valid_quantities = valid_quantities
        self.cached_number_available = cached_number_available

    @classmethod
    def from_api_data(cls, data):
        """Creates AvailabilityDetails from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns availability details.

        Returns:
            list: a list of
            :class:`AvailabilityDetails <pyticketswitch.availability.AvailabilityDetails>`
            objects populated with the data from the api.

        """
        details = []

        for ticket_type in data.get('ticket_type', []):
            kwargs = {
                'ticket_type': ticket_type.get('ticket_type_code'),
                'ticket_type_description': ticket_type.get('ticket_type_desc'),
            }

            for price_band in ticket_type.get('price_band', []):
                kwargs.update(
                    price_band=price_band.get('price_band_code'),
                    price_band_description=price_band.get('price_band_desc'),
                )

                raw_details_list = price_band.get('avail_detail', [{}])

                for raw_details in raw_details_list:

                    kwargs['seatprice'] = raw_details.get('seatprice', 0.0)
                    kwargs['full_seatprice'] = raw_details.get('full_seatprice', 0.0)
                    kwargs['surcharge'] = raw_details.get('surcharge', 0.0)
                    kwargs['full_surcharge'] = raw_details.get('full_surcharge', 0.0)
                    kwargs['percentage_saving'] = raw_details.get('percentage_saving', 0.0)
                    kwargs['absolute_saving'] = raw_details.get('absolute_saving', 0.0)
                    kwargs['currency'] = raw_details.get('avail_currency_code')

                    available_dates = raw_details.get('available_dates', {})
                    if 'first_yyyymmdd' in available_dates:
                        try:
                            first = datetime.datetime.strptime(
                                available_dates['first_yyyymmdd'],
                                '%Y%m%d'
                            )
                            kwargs['first_date'] = first.date()
                        except ValueError:
                            pass

                    if 'last_yyyymmdd' in available_dates:
                        try:
                            last = datetime.datetime.strptime(
                                available_dates['last_yyyymmdd'],
                                '%Y%m%d'
                            )
                            kwargs['last_date'] = last.date()
                        except ValueError:
                            pass

                    kwargs['calendar_masks'] = {
                        int(year[5:]): {
                            MONTH_NUMBERS[month[:3]]: mask
                            for month, mask in month_masks.items()
                        }
                        for year, month_masks in available_dates.items()
                        if year.startswith('year_')
                    }

                    if 'available_weekdays_bitmask' in raw_details:
                        kwargs['weekday_mask'] = raw_details['available_weekdays_bitmask']

                    if 'valid_quantities' in raw_details:
                        kwargs['valid_quantities'] = raw_details['valid_quantities']

                    kwargs['cached_number_available'] = (
                        raw_details.get('cached_number_available'))

                    avail_details = AvailabilityDetails(**kwargs)

                    if avail_details._weekday_mask:
                        weekday_list = []
                        for day in range(0, 7):
                            weekday_list.append(avail_details.on_weekday(day))
                        avail_details.weekday_list = weekday_list
                    details.append(avail_details)

        return sorted(details, key=lambda x: (x.ticket_type_description, x.combined_price()))

    def is_available(self, year, month=None, day=None):
        """Check availablity on a given year/month/day.

        Args:
            year (int): the year to check. For example, 2005, 2016, 2222, etc
            month (int): (optional) the month to check. 1 == jan, 12 == dec, etc
            day (int): (optional) the day of the month, zero indexed.

        Returns:
            bool: :obj:`True` when availble inside the given parameters, other
            wise :obj:`False`.

        Raises:
            ValueError: when a day is specified but not the month.

        """
        if day and not month:
            raise ValueError('a month must be specified to specify a day')

        if year not in self._calendar_masks:
            return False

        year_data = self._calendar_masks[year]

        if month and month not in year_data:
            return False

        month_mask = year_data.get(month)

        # the month mask is a 32 bit int where the right most bit is the first
        # day of the month. To find if we have availability on a specfic day,
        # we bit shift the mask by the zero indexed day and AND it by 1. If the
        # result is a 1 then this combo of ticket type and price band is
        # available on that day, otherwise it is not.
        if day and (month_mask >> (day - 1) & 1) == 0:
            return False

        return True

    def on_weekday(self, day):
        """
        Check if this combination of ticket_type and price band is available
        on a given day of the week, where 0 is monday and sunday is 6.

        .. note:: the api uses sunday as day 0 where as python uses monday.
                  I've made a concious decision here to use the python numbers
                  to keep it consistant with anything written against this.
                  (also sunday as day 0 is silly)

        Args:
            day: the day of the week zero indexed from monday.

        Returns:
            bool: :obj:`True` when available on the given day of the week,
            otherwise :obj:`False`.

        """

        adjusted_day = day + 1 if day < 6 else 0

        return bool(self._weekday_mask >> adjusted_day & 1)

    def combined_price(self):
        return self.seatprice + self.surcharge

    def combined_full_price(self):
        return self.full_seatprice + self.full_surcharge
