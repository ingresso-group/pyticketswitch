from __future__ import annotations

from typing import Any

from pyticketswitch.mixins import JSONMixin


class Media(JSONMixin):
    """Describes some event media asset

    Attributes:
        caption (str): caption in plain text describing the asset.
        caption_html (str): caption as html describing the asset.
        name (str): name of the asset.
        url (str): url for the asset.
        secure (bool): indicates if the assert url is secure or not.
        width (int): width of the asset in pixels. Only present on the video
        height (int): height of the asset in pixels. Only present on the video
            asset.

    """

    def __init__(
        self,
        caption: str | None = None,
        caption_html: str | None = None,
        name: str | None = None,
        url: str | None = None,
        secure: bool | None = None,
        width: int | None = 0,
        height: int | None = 0,
    ) -> None:

        self.caption = caption
        self.caption_html = caption_html
        self.name = name
        self.url = url
        self.secure = secure
        self.width = width
        self.height = height

    @classmethod
    def from_api_data(cls, data: dict[str, Any]) -> Media:
        """Creates a new Media object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a media asset.

        Returns:
            :class:`Media <pyticketswitch.media.Media>`: a new
            :class:`Media <pyticketswitch.media.Media>` object
            populated with the data from the api.

        """
        url = data.get("secure_complete_url")
        secure = True
        if not url:
            url = data.get("insecure_complete_url")
            secure = False

        kwargs = {
            "caption": data.get("caption"),
            "caption_html": data.get("caption_html"),
            "name": data.get("name"),
            "url": url,
            "secure": secure,
            "width": data.get("width"),
            "height": data.get("height"),
        }

        return cls(**kwargs)
