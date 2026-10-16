from __future__ import annotations

import datetime
from typing import Any

from pyticketswitch.mixins import JSONMixin
from pyticketswitch.utils import isostr_to_datetime


class Review(JSONMixin):
    """User or Critic evaluation of an event.

    Attributes:
        body (str): review test.
        date_time (datetime.datetime): date and time of the review.
        star_rating (int): rating on a scale of 1-5, with 1 being the lowest
            rating and 5 being the highest rating.
        language (str): the IETF language tag for the review.
        title (str): a review title if available.
        is_user (bool): the review was made by a user not a critic.
        author (str): the authors name.
        url (str): the original url.

    """

    def __init__(
        self,
        body: str | None = None,
        date_time: datetime.datetime | None = None,
        star_rating: int | None = None,
        lang: str | None = None,
        title: str | None = None,
        is_user: bool = False,
        author: str | None = None,
        url: str | None = None,
    ) -> None:

        self.body = body
        self.date_time = date_time
        self.star_rating = star_rating
        self.language = lang
        self.title = title
        self.is_user = is_user
        self.author = author
        self.url = url

    @classmethod
    def from_api_data(cls, data: dict[str, Any]) -> Review:
        """Creates a new **Review** object from ticketswitch API data.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a review.

        Returns:
            :class:`Review <pyticketswitch.order.Review>`: a new
            :class:`Review <pyticketswitch.order.Review>` object
            populated with the data from the api.

        """

        review_date = isostr_to_datetime(data.get("review_iso8601_date_and_time"))

        kwargs = {
            "body": data.get("review_body"),
            "date_time": review_date,
            "star_rating": data.get("star_rating"),
            "lang": data.get("review_lang"),
            "title": data.get("review_title"),
            "is_user": data.get("is_user_review", False),
            "author": data.get("review_author"),
            "url": data.get("review_original_url"),
        }

        return cls(**kwargs)
