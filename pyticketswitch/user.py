class User(object):

    def __init__(self, id_, name=None, country=None, sub_user=None,
                 is_b2b=False, statement_descriptor=None,
                 backend_group=None, content_group=None):

        self.id = id_
        self.name = name
        self.country = country
        self.sub_user = sub_user
        self.is_b2b = is_b2b
        self.statement_descriptor = statement_descriptor
        self.backend_group = backend_group
        self.content_group = content_group

    @classmethod
    def from_api_data(cls, data):

        return cls(
            data.get('user_id'),
            name=data.get('real_name'),
            country=data.get('default_country_code'),
            sub_user=data.get('sub_user'),
            is_b2b=data.get('is_b2b'),
            statement_descriptor=data.get('statement_descriptor'),
            backend_group=data.get('backend_group'),
            content_group=data.get('content_group'),
        )
