from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from requests import Response

    from pyticketswitch.currency import CurrencyMeta
    from pyticketswitch.reservation import Reservation


class PyticketswitchError(Exception):
    pass


class APIError(PyticketswitchError):
    def __init__(
        self,
        msg: str,
        code: int | None = None,
        response: Response | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(msg, *args, **kwargs)
        self.msg = msg
        self.code = code
        self.response = response


class AuthenticationError(APIError):
    pass


class InvalidParametersError(PyticketswitchError):
    pass


class InvalidResponseError(PyticketswitchError):
    pass


class InvalidGeoParameters(PyticketswitchError):
    pass


class IntegrityError(PyticketswitchError):
    def __init__(self, message: Any, data: Any, *args: Any) -> None:
        super().__init__(message, *args)
        self.data = data


class BackendError(PyticketswitchError):
    pass


class BackendBrokenError(BackendError):
    pass


class BackendDownError(BackendError):
    pass


class BackendThrottleError(BackendError):
    pass


class CallbackGoneError(APIError):
    pass


class OrderUnavailableError(PyticketswitchError):
    def __init__(
        self,
        msg: str,
        reservation: Reservation | None = None,
        meta: CurrencyMeta | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(msg, *args, **kwargs)
        self.reservation = reservation
        self.meta = meta
