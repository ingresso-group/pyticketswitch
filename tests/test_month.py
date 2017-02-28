from pyticketswitch.month import Month


class TestMonth:

    def test_from_api_data(self):
        data = {
            'month': 'nov',
            'year': 2018,
            'month_dates_bitmask': 1065254912,
            'month_desc': 'November',
            'month_weekdays_bitmask': 63,
        }

        month = Month.from_api_data(data)

        assert month.month == 11
        assert month.year == 2018
        assert month.description == 'November'
        assert month._dates_bitmask == 1065254912
        assert month._weekday_bitmask == 63

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
