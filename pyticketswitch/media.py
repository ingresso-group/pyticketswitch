from pyticketswitch.mixins import JSONMixin


class Media(JSONMixin, object):

    def __init__(self, caption=None, caption_html=None, name=None, url=None,
                 secure=None, width=0, height=0):

        self.caption = caption
        self.caption_html = caption_html
        self.name = name
        self.url = url
        self.secure = secure
        self.width = width
        self.height = height

    @classmethod
    def from_api_data(cls, data):
        url = data.get('secure_complete_url', None)
        secure = True
        if not url:
            url = data.get('insecure_complete_url', None)
            secure = False

        kwargs = {
            'caption': data.get('caption', None),
            'caption_html': data.get('caption_html', None),
            'name': data.get('name', None),
            'url': url,
            'secure': secure,
            'width': data.get('width', 0),
            'height': data.get('height', 0),
        }

        return cls(**kwargs)
