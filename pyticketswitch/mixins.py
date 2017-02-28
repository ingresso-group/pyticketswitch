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
