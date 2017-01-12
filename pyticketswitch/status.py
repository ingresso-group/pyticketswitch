from pyticketswitch.trolley import Trolley
from pyticketswitch.utils import isostr_to_datetime


class Status(object):

    def __init__(self, status=None, reserved_at=None, trolley=None,
                 purchased_at=None, external_sale_page=None,
                 languages=None, remote_site=None):
        self.status = status
        self.reserved_at = reserved_at
        self.purchased_at = purchased_at
        self.trolley = trolley
        self.external_sale_page = external_sale_page
        self.languages = languages
        self.remote_site = remote_site

    @classmethod
    def from_api_data(cls, data):

        kwargs = {
            'status': data.get('transaction_status'),
            'trolley': Trolley.from_api_data(data),
            'remote_site': data.get('remote_site'),
        }

        reserved_raw = data.get('reserve_iso8601_date_and_time')
        if reserved_raw:
            kwargs.update(reserved_at=isostr_to_datetime(reserved_raw))

        purchased_raw = data.get('purchase_iso8601_date_and_time')
        if purchased_raw:
            kwargs.update(purchased_at=isostr_to_datetime(purchased_raw))

        external_sale_page_raw = data.get('external_sale_page_raw')
        if external_sale_page_raw:
            raise NotImplemented("don't know what this looks like yet")

        languages_raw = data.get('language_list')
        if languages_raw:
            kwargs.update(languages=languages_raw.split(','))

        return cls(**kwargs)
