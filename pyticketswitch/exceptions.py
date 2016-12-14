class PyticketswitchError(Exception):
    pass


class AuthenticationError(PyticketswitchError):
    pass


class InvalidParametersError(PyticketswitchError):
    pass


class InvalidResponseError(PyticketswitchError):
    pass


class InvalidGeoData(PyticketswitchError):
    pass


class IntegrityError(PyticketswitchError):

    def __init__(self, message, data, *args):
        super(IntegrityError, self).__init__(message, *args)
        self.data = data


class EndPointMissingError(PyticketswitchError):

    def __init__(self, message, method, *args):
        super(EndPointMissingError, self).__init__(message, *args)
        self.method = method


class BackendError(PyticketswitchError):
    pass


class BackendBrokenError(BackendError):
    pass


class BackendDownError(BackendError):
    pass


class BackendThrottleError(BackendError):
    pass
