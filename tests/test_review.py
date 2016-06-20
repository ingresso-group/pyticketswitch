from pyticketswitch.review import Review


class TestReview:

    def test_from_api_data(self):

        data = {
            'review_body': 'BODY',
            'review_iso8601_date_and_time': '2013-03-30T12:00:00Z',
            'star_rating': 4,
            'review_lang': 'en',
            'review_title': '',
            'is_user_review': False,
            'review_author': "What's on Stage",
            'review_original_url': 'http://www.whatsonstage.com/index.php?pg=207&story=E01822737494'
        }

        review = Review.from_api_data(data)
        assert review.body == 'BODY'
        assert review.date_time.date().year == 2013
        assert review.date_time.date().month == 3
        assert review.date_time.date().day == 30
        assert review.star_rating == 4
        assert review.language == 'en'
        assert review.author == "What's on Stage"
        assert review.url == 'http://www.whatsonstage.com/index.php?pg=207&story=E01822737494'
        assert review.is_user is False
