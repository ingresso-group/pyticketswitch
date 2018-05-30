class PyticketswitchError(Exception):
    pass


class APIError(PyticketswitchError):
    def __init__(self, msg, code=None, response=None, *args, **kwargs):
        super(APIError, self).__init__(msg, *args, **kwargs)
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

    def __init__(self, message, data, *args):
        super(IntegrityError, self).__init__(message, *args)
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

    def __init__(self, msg, reservation=None, meta=None, *args, **kwargs):
        super(OrderUnavailableError, self).__init__(msg, *args, **kwargs)
        self.reservation = reservation
        self.meta = meta
