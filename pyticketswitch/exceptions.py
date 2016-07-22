class PyTicketSwitchError(Exception):
    pass


class AuthenticationError(PyTicketSwitchError):
    pass


class InvalidParametersError(PyTicketSwitchError):
    pass


class InvalidResponseError(PyTicketSwitchError):
    pass


class IntegrityError(PyTicketSwitchError):

    def __init__(self, *args, data=None):
        super(IntegrityError, self).__init__(*args)
        self.data = data


class EndPointMissingError(PyTicketSwitchError):

    def __init__(self, *args, method=None):
        super(EndPointMissingError, self).__init__(*args)
        self.method = method
