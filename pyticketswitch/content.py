from __future__ import annotations

from typing import Any

from pyticketswitch.mixins import JSONMixin


class Content(JSONMixin):
    """Plain text and HTML content

    Attributes:
        name (str): the identifier of the content
        value (str): plain text content.
        value_html (str): html content.

    """

    def __init__(
        self,
        name: str | None = None,
        value: str | None = None,
        value_html: str | None = None,
    ) -> None:

        self.name = name
        self.value = value
        self.value_html = value_html

    @classmethod
    def from_api_data(cls, data: dict[str, Any]) -> Content:
        """Creates a new Content object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns some content..

        Returns:
            :class:`Content <pyticketswitch.content.Content>`: a new
            :class:`Content <pyticketswitch.content.Content>` object
            populated with the data from the api.

        """

        kwargs = {
            "name": data.get("name"),
            "value": data.get("value"),
            "value_html": data.get("value_html"),
        }

        return cls(**kwargs)
