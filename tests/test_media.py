from pyticketswitch.media import Media


class TestMedia:

    def test_from_api_data_secure(self):
        data = {
            'caption_html': '<BR>',
            'name': 'landscape',
            'secure_complete_url': 'https://testurl.com',
            'supports_http': True,
            'caption': 'caption',
            'host': 'd1wx4w35ubmdix.cloudfront.net',
            'supports_https': True,
            'path': '/shared/event_media/cropper_cloud/24/249fdb60b56ef4217a6049a1ed770f13552bca9c.jpg',
            'insecure_complete_url': 'http://testurl.com',
        }

        media = Media.from_api_data(data)
        assert media.url == 'https://testurl.com'
        assert media.caption_html == '<BR>'
        assert media.caption == 'caption'
        assert media.name == 'landscape'
        assert media.secure is True

    def test_from_api_data_insecure(self):
        data = {
            'caption_html': '<BR>',
            'name': 'landscape',
            'secure_complete_url': '',
            'supports_http': False,
            'caption': 'caption',
            'host': 'd1wx4w35ubmdix.cloudfront.net',
            'supports_https': True,
            'path': '/shared/event_media/cropper_cloud/24/249fdb60b56ef4217a6049a1ed770f13552bca9c.jpg',
            'insecure_complete_url': 'http://testurl.com',
        }

        media = Media.from_api_data(data)
        assert media.url == 'http://testurl.com'
        assert media.secure is False
