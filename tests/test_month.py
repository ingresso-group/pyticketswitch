import datetime
from pyticketswitch.month import Month


class TestMonth:

    def test_from_api_data(self):
        data = {
            'month': 'nov',
            'year': 2018,
            'month_dates_bitmask': 1065254912,
            'month_desc': 'November',
            'month_weekdays_bitmask': 63,
            'cost_range': {
                'range_currency_code': 'gbp',
                'valid_quantities': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'max_surcharge': 39.45,
                'max_seatprice': 197.25,
                'min_surcharge': 5.4,
                'min_seatprice': 20.0,
                'no_singles_cost_range': {
                    'range_currency_code': 'gbp',
                    'valid_quantities': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'max_surcharge': 39.45,
                    'max_seatprice': 197.25,
                    'min_surcharge': 5.4,
                    'min_seatprice': 30.0
                },
            }
        }

        month = Month.from_api_data(data)

        assert month.month == 11
        assert month.year == 2018
        assert month.description == 'November'
        assert month._dates_bitmask == 1065254912
        assert month._weekday_bitmask == 63
        assert month.cost_range.min_seatprice == 20.00
        assert month.cost_range.currency == 'gbp'
        assert month.no_singles_cost_range.min_seatprice == 30.00
        assert month.cost_range.currency == 'gbp'

    def test_from_api_data_without_cost_range(self):
        data = {
            'month': 'nov',
            'year': 2018,
            'month_dates_bitmask': 1065254912,
            'month_desc': 'November',
            'month_weekdays_bitmask': 63
        }

        month = Month.from_api_data(data)

        assert month.month == 11
        assert month.year == 2018
        assert month.description == 'November'
        assert month._dates_bitmask == 1065254912
        assert month._weekday_bitmask == 63
        assert month.cost_range is None
        assert month.no_singles_cost_range is None

    def test_is_available(self):
        # 1065254912 == 111111011111101000000000000000
        assert Month(0, 0, dates_bitmask=1065254912).is_available(1) is False
        assert Month(0, 0, dates_bitmask=1065254912).is_available(15) is False
        assert Month(0, 0, dates_bitmask=1065254912).is_available(16) is True
        assert Month(0, 0, dates_bitmask=1065254912).is_available(17) is False
        assert Month(0, 0, dates_bitmask=1065254912).is_available(23) is True
        assert Month(0, 0, dates_bitmask=1065254912).is_available(24) is False

    def test_on_weekday(self):
        # 85 == 1010101, and we add one to the index so monday is 0 rather than
        # sunday like in the api
        assert Month(0, 0, weekday_bitmask=85).on_weekday(0) is False
        assert Month(0, 0, weekday_bitmask=85).on_weekday(1) is True
        assert Month(0, 0, weekday_bitmask=85).on_weekday(2) is False
        assert Month(0, 0, weekday_bitmask=85).on_weekday(3) is True

    def test_start_date(self):
        # 1065254912 == 111111011111101000000000000000, and we add one to the index so monday is 0 rather than
        # sunday like in the api
        sixteenth_of_january = datetime.date(2020, 1, 16)
        assert Month(1, 2020, dates_bitmask=1065254912).start_date() == sixteenth_of_january

    def test_start_date_with_none(self):
        assert Month(1, 2020, dates_bitmask=None).start_date() is None

    def test_end_date(self):
        # 2130509824 == 1111110111111010000000000000000
        thirty_first_of_march = datetime.date(2020, 3, 31)
        assert Month(3, 2020, dates_bitmask=2130509824).end_date() == thirty_first_of_march

    def test_end_date_with_none(self):
        assert Month(1, 2020, dates_bitmask=None).end_date() is None
