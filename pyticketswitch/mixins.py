import datetime
import json


class JSONMixin(object):
    """Adds json encoding functionality to objects."""

    def __jsondict__(self, hide_none=True, hide_empty=True):

        def sanitise(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()

            if isinstance(obj, datetime.date):
                return obj.isoformat()

            if hasattr(obj, '__jsondict__'):
                return obj.__jsondict__(hide_none=hide_none, hide_empty=hide_empty)

            if isinstance(obj, list):
                return [sanitise(item) for item in obj]

            if isinstance(obj, dict):
                return {key: sanitise(value) for key, value in obj.items()}

            return obj

        return {
            key: sanitise(obj)
            for key, obj in self.__dict__.items()

            # when hiding None's and the object is None, skip the object
            if not (hide_none and obj is None)

            # when hiding empty iterators and the object is an iterator and
            # it's empty, skip the object.
            if not (hide_empty and hasattr(obj, '__iter__') and not obj)
        }

    def as_dict_for_json(self, hide_none=True, hide_empty=True):
        """Generate a json serialisable dictionary from the object

        Dates are changed to strings in ISO 8601 format.

        Lists children are recursively serialised.

        Dictionary values are recursively serialised, keys are left as is.

        Objects that implement __jsondict__ return the result of calling
        __jsondict__ on the object.

        Args:
            hide_none (bool, optional): when :obj:`True` the returned
                dictionary will not include attributes who's value is
                :obj:`None`.
            hide_empty (bool, optional): when :obj:`True` the returned
                dictionary will not include attributes who's value is iterable
                and has a length of zero.

        Returns:
            dict: a dictionary representation of the object.

        """
        return self.__jsondict__(hide_none=hide_none, hide_empty=hide_empty)

    def as_json(self, hide_none=True, hide_empty=True, **kwargs):
        """Generate a json represetation of an object.

        Args:
            hide_none (bool, optional): when :obj:`True` the returned
                dictionary will not include attributes who's value is
                :obj:`None`.
            hide_empty (bool, optional): when :obj:`True` the returned
                dictionary will not include attributes who's value is iterable
                and has a length of zero.
            **kwargs: passed to :py:func:`json.dumps`.

        Returns:
            str: a json representation of an object

        """

        return json.dumps(
            self.as_dict_for_json(hide_none=hide_none, hide_empty=hide_empty),
            **kwargs
        )


class PaginationMixin(object):
    """Adds pagination information to a responses meta data.

    Attributes:
        page_length (int): the number of items per page.
        page_number (int): the current page.
        pages_remaining (int): the number of pages remaining.
        results_remaining (int): the total number of remaining results after
            the current page.
        total_results (int): the total number of results.

    """

    def __init__(self, page_length=None, page_number=None, pages_remaining=None,
                 total_results=None, *args, **kwargs):
        self.page_length = page_length
        self.page_number = page_number
        self.pages_remaining = pages_remaining
        self.total_results = total_results
        super(PaginationMixin, self).__init__(*args, **kwargs)

    @classmethod
    def from_api_data(cls, data, *args, **kwargs):
        inst = super(PaginationMixin, cls).from_api_data(data)

        results = data.get('results', {})
        paging_data = results.get('paging_status', {})

        inst.page_length = paging_data.get('page_length')
        inst.page_number = paging_data.get('page_number')
        inst.pages_remaining = paging_data.get('pages_remaining')
        inst.results_remaining = paging_data.get('results_remaining')
        inst.total_results = paging_data.get('total_unpaged_results')

        return inst

    def is_paginated(self):
        """Indicates that the response is paginated

        Returns:
            bool: :obj:`True` when the response is omitting results due to
            pagination otherwise :obj:``False``

        """

        if not self.total_results or not self.page_length:
            return False

        if self.total_results < self.page_length:
            return False

        return True
