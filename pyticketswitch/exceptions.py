class PyticketswitchError(Exception):
    pass


class APIError(PyticketswitchError):
    def __init__(self, msg, code, response, *args, **kwargs):
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
