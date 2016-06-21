import pytest
from datetime import date, datetime
from pyticketswitch import utils
from pyticketswitch import exceptions


class TestDateRangeStr:

    def test_date_range_str(self):
        start_date = date(2016, 6, 21)
        end_date = date(2017, 1, 1)

        date_range_str = utils.date_range_str(start_date, end_date)
        assert date_range_str == '20160621:20170101'

    def test_date_range_str_with_datetimes(self):
        start_date = datetime(2016, 6, 21, 19, 30, 15)
        end_date = datetime(2017, 1, 1, 13, 45, 30)

        date_range_str = utils.date_range_str(start_date, end_date)
        assert date_range_str == '20160621:20170101'

    def test_date_range_str_with_no_end_date(self):
        start_date = date(2016, 6, 21)
        end_date = None

        date_range_str = utils.date_range_str(start_date, end_date)
        assert date_range_str == '20160621:'

    def test_date_range_str_with_no_start_date(self):
        start_date = None
        end_date = date(2017, 1, 1)

        date_range_str = utils.date_range_str(start_date, end_date)
        assert date_range_str == ':20170101'

    def test_date_range_str_with_no_start_date_or_end_date(self):
        start_date = None
        end_date = None

        date_range_str = utils.date_range_str(start_date, end_date)
        assert date_range_str == ''

    def test_date_range_str_with_invalid_end_date(self):
        start_date = date(2016, 6, 21)
        end_date = 'FOOBAR!'

        with pytest.raises(exceptions.InvalidParametersError):
            utils.date_range_str(start_date, end_date)

    def test_date_range_str_with_invalid_start_date(self):
        start_date = 'SAUSAGES!'
        end_date = date(2017, 1, 1)
        with pytest.raises(exceptions.InvalidParametersError):
            utils.date_range_str(start_date, end_date)
