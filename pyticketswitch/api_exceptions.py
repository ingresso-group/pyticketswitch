# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from pyticketswitch.util import resolve_boolean


class APIException(Exception):
    """General Exception object for representing an error returned by the API.

    Used as a super class for some other Exception objects defined here.
    """

    def __init__(
        self, call, code, description
    ):
        self.call = call
        self.code = code
        self.description = description

    def __str__(self):
        return "API Exception - call={0}, code={1}, description={2}".format(
            self.call, self.code, self.description
        )


class InvalidToken(APIException):
    """Exception indicating that the token passed to the API was invalid.

    Can also be referred to as InvalidId.
    """

    def __init__(
        self, call, description, code=None
    ):
        if code is None:
            code = "N/A"

        super(InvalidToken, self).__init__(
            call=call, code=code, description=description
        )

InvalidId = InvalidToken


class BackendCallFailure(APIException):
    """The API returned that the backend call failed.

    This indicates that there is a problem with supplier's system,
    causing the API call to fail.
    """

    def __init__(
        self, call
    ):
        code = "N/A"
        description = "The call to the backend system failed."

        super(BackendCallFailure, self).__init__(
            call=call, code=code, description=description
        )


class CommsException(Exception):
    """Thrown when there was problem communicating with the API.

    This could be a problem at the HTTP, URL or networking
    level, including a timeout (i.e. the API takes more than
    the timeout settings value to respond).
    """

    def __init__(
        self, underlying_exception, description
    ):
        self.underlying_exception = underlying_exception
        self.description = description

    def __str__(self):
        return self.description


class InvalidResponse(Exception):
    """The response from the API could not be interpreted.

    This is thrown when the data returned by the API cannot
    be parsed, most likely indicates a failure of the API.
    """

    def __init__(
        self, underlying_exception, description
    ):
        self.underlying_exception = underlying_exception
        self.description = description

    def __str__(self):
        return self.description


# TROLLEY ADD ERRORS
class TrolleyAddErrors(Exception):
    """Thrown when an attempt to add an Order to a Trolley fails.

    Used to represent errors returned by the 'trolley_add_order' API
    call. The string representation of the object describes the errors
    in the 'errors' list.

    There is more detail about errors when adding orders to the trolley
    in the XML API documentation.

    Attributes:
        errors (list): List of Exception objects representing errors
            returned when adding an Order to a Trolley.
    """

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return ', '.join([str(type(error)) for error in self.errors])


class TrolleyAddBadBundle(Exception):
    """Reached the maximum number of orders for the supplier's system.

    Attributes:
        max_size (int): The maximum number of orders this supplier allows
            per transaction.
    """

    def __init__(
        self, max_size
    ):
        self.max_size = max_size

    def __str__(self):
        return "Trolley can only contain {0} orders from this supplier".format(
            self.max_size
        )


class TrolleyAddBadCombo(Exception):
    """Order could not be added to the trolley because the mix of suppliers
    is not allowed.

    Attributes:
        system (string): Code of existing supplier.
        system_desc (string): Name of existing supplier.
    """

    def __init__(self, system, system_desc):
        self.system = system
        self.system_desc = system_desc

    def __str__(self):
        return (
            "Supplier is not compatible with {1} ({0}), which is " +
            "currently in the trolley"
        ).format(
            self.system, self.system_desc
        )


class TrolleyAddBadCardTypes(Exception):
    """Order could not be added because there are no compatible card types
    between suppliers.
    """

    def __str__(self):
        return "No compatible card types between suppliers"


class TrolleyAddBadCountries(Exception):
    """Order could not be added due to incompatible countries allowed by the
    suppliers."""

    def __str__(self):
        return "Incompatible allowed countries"


class TrolleyAddBadCurrencyMix(Exception):
    """Order could not be added as there is an existing order for this supplier
    in the trolley with a different currency."""

    def __init__(
        self, system, system_desc, currency, currency_name
    ):
        self.system = system
        self.system_desc = system_desc
        self.currency = currency
        self.currency_name = currency_name

    def __str__(self):
        return "Currency conflicts with existing order on {1} ({0})".format(
            self.system, self.system_desc
        )


class TrolleyAddBadDepart(Exception):
    """Order could not be added due to incompatible departure dates."""

    def __str__(self):
        return "Incompatible departure dates"


class TrolleyAddBadSend(Exception):
    """Order could not be added due to incompatible despatch methods."""

    def __str__(self):
        return "Incompatible despatch methods"
# END TROLLEY ADD ERRORS


# TROLLEY ERRORS
class TrolleyPurchased(APIException):
    """Thrown when the operation attempted is not possible as the trolley has
    already been purchased."""
    pass


class TrolleyReserved(APIException):
    """Thrown when the operation attempted is not possible as the trolley has
    already been reserved."""
    pass


class NoAvailability(APIException):
    """Thrown when the operation failed due to there no longer being
    availability for the seats."""

    def __init__(
        self, call
    ):
        self.call = call
        code = "N/A"
        description = "The call returned no availability"

        super(NoAvailability, self).__init__(
            call=call, code=code, description=description
        )
# END TROLLEY ERRORS


# PURCHASE ERRORS
class PurchaseValidationError(APIException):
    """Super class for purchase validation errors."""
    pass


class InvalidCountryForDespatch(PurchaseValidationError):
    """The chosen despatch method does not allow the given country code
    in the customer data (XML API code 1306)."""
    pass


class InvalidEmailAddress(PurchaseValidationError):
    """The supplied email address failed RFC822 syntax checking
    (XML API code 1307)."""
    pass


class IncompleteCustomerDetails(PurchaseValidationError):
    """The customer details supplied are incomplete (XML API code 1308)."""
    pass


class NoCardNumberProvided(PurchaseValidationError):
    """No card_number element was present in the payment card data
    (XML API code 1309)."""
    pass


class UnknownCardType(PurchaseValidationError):
    """The payment card type is not known from the supplied card number
    (XML API code 1310)."""
    pass


class InvalidCardType(PurchaseValidationError):
    """The payment card type is not one of those accepted for this
    transaction (XML API code 1311)."""
    pass


class InvalidCardNumber(PurchaseValidationError):
    """The card number given is not valid for cards of that type
    (XML API code 1312)."""
    pass


class NoExpiryDateProvided(PurchaseValidationError):
    """No "expiry_date" element was present in the payment card data
    (XML API code 1313)."""
    pass


class InvalidExpiryDate(PurchaseValidationError):
    """The expiry date given is not valid (XML API code 1314)."""
    pass


class NoCV2Provided(PurchaseValidationError):
    """No 'cv_two' was present in the payment card data (XML API code 1315)."""
    pass


class InvalidCV2(PurchaseValidationError):
    """The CV2 value given is not valid (XML API code 1316)."""
    pass


class NoIssueNumberProvided(PurchaseValidationError):
    """No 'issue_number' has been supplied when required (XML API code 1317).
    """
    pass


class InvalidIssueNumber(PurchaseValidationError):
    """The issue number given is not valid (XML API code 1319)."""
    pass


class IncompleteAltBillingAddress(PurchaseValidationError):
    """The billing address details supplied are incomplete
    (XML API code 1321)."""
    pass


class NoStartDateProvided(PurchaseValidationError):
    """No 'start_date' element has been supplied when required
    (XML API code 1322)."""
    pass


class InvalidStartDate(PurchaseValidationError):
    """The start date given is not valid (XML API code 1323)."""
    pass


class ReservationExpired(APIException):
    """Operation failed because the reservation has expired
    (XML API code 1404)."""
    pass


class PurchaseException(APIException):
    """General Exception class for purchase errors.

    This class is sub classed by several Exception classes.
    """
    def __init__(
        self, call, description, code=None, failed_cv_two=None,
        failed_avs=None, failed_3d_secure=None
    ):
        self._failed_cv_two = failed_cv_two
        self._failed_avs = failed_avs
        self._failed_3d_secure = failed_3d_secure

        super(PurchaseException, self).__init__(
            call=call, code=code, description=description
        )

    @property
    def failed_cv_two(self):
        """Boolean to indicate if the purchase attempt was marked with a
        CV2 failure."""
        return resolve_boolean(self._failed_cv_two)

    @property
    def failed_avs(self):
        """Boolean to indicate if the purchase attempt was marked with a
        AVS failure."""
        return resolve_boolean(self._failed_avs)

    @property
    def failed_3d_secure(self):
        """Boolean to indicate if the purchase attempt was marked with a
        3D secure failure."""
        return resolve_boolean(self._failed_3d_secure)


class FraudTriggered(PurchaseException):
    """The combination of customer and payment card details have matched a
    system fraud trigger and the purchase has not be allowed.

    (XML API purchase_fail_code 1).
    """
    pass


class CardAuthorisationFailed(PurchaseException):
    """The payment card provided could not be authorised for the value of
    the transaction or the authorisation timed out.

    (XML API purchase_fail_code 2, 3).
    """
    pass


class ReservationAlreadyPurchased(PurchaseException):
    """The reservation has already been purchased (XML API
    purchase_fail_code 4)."""
    pass


class PurchasePreviouslyAttempted(PurchaseException):
    """The reservation purchase has already been attempted and failed
    (XML API purchase_fail_code 5)."""
    pass


class PurchaseRefused(PurchaseException):
    """The reservation purchase has been refused by the backend
    (XML API purchase_fail_code 6)."""
    pass


# 7 - an unspecified systems error has occurred during purchase
class PurchaseFailed(PurchaseException):
    """An unspecified systems error has occurred during purchase
    (XML API purchase_fail_code 7)."""
    pass
# END PURCHASE ERRORS
