import datetime


class Review(object):

    def __init__(self, body=None, date_and_time=None, rating=None,
                 lang=None, title=None, is_user=False, author=None, url=None):

        self.body = body
        self.date_and_time = date_and_time
        self.rating = rating
        self.language = lang
        self.title = title
        self.is_user = is_user
        self.author = author
        self.url = url

    @classmethod
    def from_api_data(cls, data):

        review_date = datetime.datetime.strptime(
            data.get('review_iso8601_date_and_time', '0000-00-00T00:00:00Z'),
            "%Y-%m-%dT%H:%M:%SZ",
        )

        kwargs = {
            'body': data.get('review_body', None),
            'date_and_time': review_date,
            'rating': data.get('star_rating', None),
            'lang': data.get('review_lang', None),
            'title': data.get('review_title', None),
            'is_user': data.get('is_user_review', False),
            'author': data.get('review_author', None),
            'url': data.get('review_original_url', None),
        }

        return cls(**kwargs)
