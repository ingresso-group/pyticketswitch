import datetime
import json


class JSONMixin(object):

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
            if not (hide_none and obj is None)
            if not (hide_empty and hasattr(obj, '__iter__') and not obj)
        }

    def as_dict_for_json(self, hide_none=True, hide_empty=True):
        return self.__jsondict__(hide_none=hide_none, hide_empty=hide_empty)

    def as_json(self, hide_none=True, hide_empty=True, **kwargs):
        return json.dumps(
            self.as_dict_for_json(hide_none=hide_none, hide_empty=hide_empty),
            **kwargs
        )
