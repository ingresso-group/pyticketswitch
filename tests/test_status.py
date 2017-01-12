import datetime
from pyticketswitch.status import Status
from dateutil.tz import tzoffset


class TestStatus:

    ZULU = tzoffset('ZULU', 0)

    def test_from_api_data(self):

        data = {
            'external_sale_page': {},
            'language_list': 'en-gb,en,en-us,nl',
            'remote_site': 'foobar.example.com',
            'reserve_iso8601_date_and_time': '2016-11-09T18:19:27Z',
            'purchase_iso8601_date_and_time': '2016-11-11T12:34:49Z',
            'transaction_status': 'purchased',
            'trolley_contents': {
                'transaction_uuid': '284d9c3a-d698-11e6-be8c-002590326962',
            }
        }

        status = Status.from_api_data(data)

        assert status.status == 'purchased'
        assert status.reserved_at == datetime.datetime(2016, 11, 9, 18, 19, 27, tzinfo=self.ZULU)
        assert status.purchased_at == datetime.datetime(2016, 11, 11, 12, 34, 49, tzinfo=self.ZULU)
        assert status.external_sale_page is None
        assert status.languages == ['en-gb', 'en', 'en-us', 'nl']
        assert status.remote_site == 'foobar.example.com'
        assert status.trolley.transaction_uuid == '284d9c3a-d698-11e6-be8c-002590326962'
