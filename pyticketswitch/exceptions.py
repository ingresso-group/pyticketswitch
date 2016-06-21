class PyTicketSwitchError(Exception):
    pass


class AuthenticationError(PyTicketSwitchError):
    pass


class InvalidParametersError(PyTicketSwitchError):
    pass


class InvalidResponseError(PyTicketSwitchError):
    pass


class IntegrityError(PyTicketSwitchError):

    def __init__(self, data=None, *args):
        super(IntegrityError, self).__init__(*args)
        self.data = data


class EndPointMissingError(PyTicketSwitchError):

    def __init__(self, method=None, *args):
        super(EndPointMissingError, self).__init__(*args)
        self.method = method
