class PyTicketSwitchError(Exception):
    pass


class AuthenticationError(PyTicketSwitchError):
    pass


class InvalidParametersError(PyTicketSwitchError):
    pass


class InvalidResponseError(PyTicketSwitchError):
    pass


class IntegrityError(PyTicketSwitchError):

    def __init__(self, message, data, *args):
        super(IntegrityError, self).__init__(message, *args)
        self.data = data


class EndPointMissingError(PyTicketSwitchError):

    def __init__(self, message, method, *args):
        super(EndPointMissingError, self).__init__(message, *args)
        self.method = method
