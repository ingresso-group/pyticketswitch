from pyticketswitch.exceptions import IntegrityError
from pyticketswitch.interface.cost_range import CostRange
from pyticketswitch.interface.ticket_type import TicketType
from pyticketswitch.interface.content import Content
from pyticketswitch.interface.media import Media
from pyticketswitch.interface.review import Review
from pyticketswitch import utils


class Event(object):

    def __init__(self, event_id, status=None, event_type=None, source=None,
                 venue=None, description=None, postcode=None, classes=None,
                 filters=None, start_date=None, end_date=None,
                 upsell_list=None, city=None, country=None, country_code=None,
                 latitude=None, longditude=None, needs_departure_date=False,
                 needs_duration=False, needs_performance=False,
                 has_performances=False, is_seated=False,
                 show_performance_time=False, min_running_time=None,
                 max_running_time=None, cost_range=None,
                 no_singles_cost_range=None, cost_range_details=None,
                 content=None, event_info_html=None, event_info=None,
                 venue_addr_html=None, venue_addr=None, venue_info=None,
                 venue_info_html=None, media=None, reviews=None,
                 availability_details=None):

        self.event_id = event_id
        self.status = status
        self.description = description
        self.source = source
        self.event_type = event_type
        self.venue = venue

        self.classes = classes
        self.filters = filters

        self.start_date = start_date
        self.end_date = end_date

        self.postcode = postcode
        self.city = city
        self.country = country
        self.country_code = country_code
        self.latitude = latitude
        self.longditude = longditude

        self.max_running_time = max_running_time
        self.min_running_time = min_running_time

        self.show_performance_time = show_performance_time
        self.has_performances = has_performances
        self.is_seated = is_seated
        self.needs_departure_date = needs_departure_date
        self.needs_duration = needs_duration
        self.needs_performance = needs_performance

        self.upsell_list = upsell_list

        self.cost_range = cost_range
        self.no_singles_cost_range = no_singles_cost_range
        self.cost_range_details = cost_range_details

        self.content = content
        self.event_info = event_info
        self.event_info_html = event_info_html
        self.venue_addr = venue_addr
        self.venue_addr_html = venue_addr_html
        self.venue_info = venue_info
        self.venue_info_html = venue_info_html

        self.media = media
        self.reviews = reviews

        self.availability_details = availability_details

    @classmethod
    def from_api_data(cls, data):

        event_id = data.get('event_id')

        if not event_id:
            raise IntegrityError("event_id not found in event data", data=data)

        start_date = data.get('date_range_start', {}).get('iso8601_date_and_time')
        if start_date:
            start_date = utils.isostr_to_datetime(start_date)

        end_date = data.get('date_range_end', {}).get('iso8601_date_and_time')
        if end_date:
            end_date = utils.isostr_to_datetime(end_date)

        classes = data.get('class', [])
        if classes:
            classes = [
                c.get('class_desc') for c in classes
                if 'class_desc' in c
            ]

        geo_data = data.get('geo_data', {})

        # the raw field 'has_no_perfs' is a negative flag, so I'm inverting it
        has_performances = not data.get('has_no_perfs', False)

        api_cost_range = data.get('cost_range', {})
        api_no_singles_cost_range = api_cost_range.get('no_singles_cost_range', {})
        cost_range = None
        no_singles_cost_range = None
        cost_range_details = []

        if api_cost_range:
            api_cost_range['singles'] = True
            cost_range = CostRange.from_api_data(api_cost_range)

        if api_no_singles_cost_range:
            api_no_singles_cost_range['singles'] = False
            no_singles_cost_range = CostRange.from_api_data(
                api_no_singles_cost_range)

        api_cost_range_details = data.get('cost_range_details', {})
        if api_cost_range_details:
            ticket_type_list = api_cost_range_details.get('ticket_type', [])
            for ticket_type in ticket_type_list:
                cost_range_details.append(TicketType.from_api_data(ticket_type))

        api_content = data.get('structured_info', {})
        content = {}
        if api_content:
            for key, value in api_content.items():
                content[key] = Content.from_api_data(value)

        api_media = data.get('media', {})
        media = []
        if api_media:
            for asset in api_media.get('media_asset', []):
                media.append(Media.from_api_data(asset))

        api_video = data.get('video_iframe', {})
        if api_video:
            kwargs = {
                'secure_complete_url': api_video.get('video_iframe_url_when_secure', None),
                'insecure_complete_url': api_video.get('video_iframe_url_when_insecure', None),
                'caption': api_video.get('video_iframe_caption', None),
                'caption_html': api_video.get('video_iframe_caption_html', None),
                'width': api_video.get('video_iframe_width', None),
                'height': api_video.get('video_iframe_height', None),
                'name': 'video',
            }
            media.append(Media.from_api_data(kwargs))

        api_reviews = data.get('reviews', {})
        reviews = []
        if api_reviews:
            for api_review in api_reviews.get('review', []):
                reviews.append(Review.from_api_data(api_review))

        api_availability = data.get('avail_details', {})
        availability_details = []
        if api_availability:
            ticket_type_list = api_availability.get('ticket_type', [])
            for ticket_type in ticket_type_list:
                availability_details.append(TicketType.from_api_data(ticket_type))
        api_meta_events = data.get('meta_event_component_events', {})
        if api_meta_events:
            for meta_event in api_meta_events.get('event', []):
                pass

        kwargs = {
            'event_id': event_id,
            'status': data.get('event_status'),
            'event_type': data.get('event_type'),
            'source': data.get('source_desc'),
            'venue': data.get('venue_desc'),

            'classes': classes,
            #TODO: don't actually know what filters look like yet...
            'filters': data.get('custom_filter', []),

            'start_date': start_date,
            'end_date': end_date,

            'postcode': data.get('postcode'),
            'city': data.get('city_desc'),
            'country': data.get('country_desc'),
            'country_code': data.get('country_code'),

            'latitude': geo_data.get('latitude'),
            'longditude': geo_data.get('longditude'),

            'max_running_time': data.get('max_running_time'),
            'min_running_time': data.get('min_running_time'),

            'has_performances': has_performances,
            'show_performance_time': data.get('show_perf_time', False),
            'is_seated': data.get('is_seated', False),
            'needs_departure_date': data.get('needs_departure_date', False),
            'needs_duration': data.get('needs_duration', False),
            'needs_performance': data.get('needs_performance', False),

            'upsell_list': data.get('event_upsell_list', {}).get('event_id', []),

            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
            'cost_range_details': cost_range_details,

            # extra info
            'event_info_html': data.get('event_info_html', None),
            'event_info': data.get('event_info', None),
            'venue_addr_html': data.get('venue_addr_html', None),
            'venue_addr': data.get('venue_addr', None),
            'venue_info': data.get('venue_info', None),
            'venue_info_html': data.get('venue_info_html', None),
            'content': content,

            'media': media,
            'reviews': reviews,

            'availability_details': availability_details,
        }

        return cls(**kwargs)
