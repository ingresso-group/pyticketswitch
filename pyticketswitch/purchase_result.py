from pyticketswitch.mixins import JSONMixin


class PurchaseResult(JSONMixin, object):
    """Describes the results of a purchase attempt

    Attributes:
        success (bool): indicates if the purchase was successful.
        failed_3d_secure (bool): indicates if the purchase failed 3d secure.
        failed_avs (bool): indicates if the purchase failed address checks.
        failed_cv_two (bool): indicates if the purchase credit card
            verification number.
        error (string): error code for backend purchase failure. These are
            non uniform as they can come from a varitiy of sources.

    """

    def __init__(self, success=False, failed_3d_secure=False, failed_avs=False,
                 failed_cv_two=False, error=None):

        self.success = success
        self.failed_3d_secure = failed_3d_secure
        self.failed_avs = failed_avs
        self.failed_cv_two = failed_cv_two
        self.error = error

    @classmethod
    def from_api_data(cls, data):
        """Creates a new PurchaseResults object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns the results of a purchase attempt.

        Returns:
            :class:`PurchaseResult <pyticketswitch.purchase_result.PurchaseResult>`:
            a new
            :class:`PurchaseResult <pyticketswitch.purchase_result.PurchaseResult>`
            object populated with the data from the api.

        """

        kwargs = {
            'success': data.get('success'),
            'failed_3d_secure': data.get('failed_3d_secure'),
            'failed_avs': data.get('failed_avs'),
            'failed_cv_two': data.get('failed_cv_two'),
            'error': data.get('purchase_error'),
        }

        return cls(**kwargs)
