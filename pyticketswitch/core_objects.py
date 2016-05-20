# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class CoreObject(object):
    pass


class CoreObjectCollection(list):

    def all(self):
        return self


class RunningUser(CoreObject):

    def __init__(
        self,
        user_id,
        style,
        real_name=None,
        sub_style=None,
        sub_sub_style=None,
        backend_group=None,
        content_group=None,
        restrict_group=None,
        sphinx_restrict_group=None,
        default_country_code=None,
        default_lang_code=None,
        **kwargs
    ):

        self.user_id = user_id
        self.style = style
        self.real_name = real_name
        self.sub_style = sub_style
        self.sub_sub_style = sub_sub_style
        self.backend_group = backend_group
        self.content_group = content_group
        self.restrict_group = restrict_group
        self.sphinx_restrict_group = sphinx_restrict_group
        self.default_country_code = default_country_code
        self.default_lang_code = default_lang_code

        vars(self).update(kwargs)


class Event(CoreObject):

    def __init__(
        self,
        event_desc,
        venue_desc,
        source_desc,
        source_code,
        event_token=None,
        event_id=None,
        venue_info=None,
        venue_addr=None,
        classes=None,
        event_medias=None,
        cost_range=None,
        city_code=None,
        city_desc=None,
        country_code=None,
        country_desc=None,
        geo_data=None,
        reviews=None,
        user_review_percent=None,
        critic_review_percent=None,
        source_t_and_c=None,
        source_after_sales_email=None,
        source_card_statement_desc=None,
        source_enquiries_email=None,
        source_local_phone=None,
        source_local_fax=None,
        source_international_phone=None,
        source_international_fax=None,
        source_postal_addr=None,
        video_iframe=None,
        custom_fields=None,
        custom_filters=None,
        is_seated=None,
        has_no_perfs=None,
        date_range_start=None,
        date_range_end=None,
        show_perf_time=None,
        need_departure_date=None,
        need_performance=None,
        need_duration=None,
        structured_info=None,
        event_quantity_options=None,
        avail_details=None,
        component_events=None,
        **kwargs
    ):

        self.event_desc = event_desc
        self.venue_desc = venue_desc
        self.source_desc = source_desc
        self.source_code = source_code
        self.event_token = event_token
        self.event_id = event_id

        if event_token is None and event_id is not None:
            self.event_token = event_id

        if self.event_id is None and self.event_token is not None:
            self.event_id = event_token

        self.venue_info = venue_info
        self.venue_addr = venue_addr
        if classes is None:
            classes = []
        self.classes = classes
        if event_medias is None:
            event_medias = []
        self.event_medias = event_medias
        self.cost_range = cost_range
        self.city_code = city_code
        self.city_desc = city_desc
        self.country_code = country_code
        self.country_desc = country_desc
        self.geo_data = geo_data
        if reviews is None:
            reviews = []
        self.reviews = reviews
        self.user_review_percent = user_review_percent
        self.critic_review_percent = critic_review_percent
        self.source_t_and_c = source_t_and_c
        self.source_after_sales_email = source_after_sales_email
        self.source_card_statement_desc = source_card_statement_desc
        self.source_enquiries_email = source_enquiries_email
        self.source_local_phone = source_local_phone
        self.source_local_fax = source_local_fax
        self.source_international_phone = source_international_phone
        self.source_international_fax = source_international_fax
        self.source_postal_addr = source_postal_addr
        self.video_iframe = video_iframe
        if custom_fields is None:
            custom_fields = []
        self.custom_fields = custom_fields
        if custom_filters is None:
            custom_filters = []
        self.custom_filters = custom_filters
        self.is_seated = is_seated
        self.has_no_perfs = has_no_perfs
        self.date_range_start = date_range_start
        self.date_range_end = date_range_end
        self.show_perf_time = show_perf_time
        self.need_departure_date = need_departure_date
        self.need_performance = need_performance
        self.need_duration = need_duration
        self.need_duration = need_duration
        if structured_info is None:
            structured_info = {}
        self.structured_info = structured_info
        self.event_quantity_options = event_quantity_options
        self.avail_details = avail_details
        if component_events is None:
            component_events = []
        self.component_events = component_events

        vars(self).update(kwargs)

    def add_extra_info(self, extra_info_event):

        for k, v in vars(extra_info_event).items():
            if v is not None:
                setattr(self, k, v)


class Class(CoreObject):

    def __init__(
        self,
        class_code,
        class_desc=None,
        is_main_class=None,
        search_key=None,
        subclasses=None,
        **kwargs
    ):

        self.class_code = class_code
        self.class_desc = class_desc
        self.is_main_class = is_main_class
        self.search_key = search_key
        if subclasses is None:
            subclasses = []
        self.subclasses = subclasses

        vars(self).update(kwargs)


class SubClass(CoreObject):
    objects = CoreObjectCollection()

    def __init__(
        self,
        subclass_code,
        subclass_desc=None,
        is_main_subclass=None,
        search_key=None,
        **kwargs
    ):
        self.subclass_code = subclass_code
        self.subclass_desc = subclass_desc
        self.is_main_subclass = is_main_subclass
        self.search_key = search_key

        vars(self).update(kwargs)

        self.objects.append(self)


class GeoData(CoreObject):

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class EventMedia(CoreObject):

    def __init__(
        self,
        name,
        path,
        host,
        secure_complete_url,
        insecure_complete_url,
        **kwargs
    ):
        self.name = name
        self.path = path
        self.host = host
        self.secure_complete_url = secure_complete_url
        self.insecure_complete_url = insecure_complete_url

        vars(self).update(kwargs)


class VideoIframe(CoreObject):

    def __init__(
        self,
        video_iframe_height,
        video_iframe_width,
        video_iframe_host,
        video_iframe_path,
        video_iframe_supports_https,
        video_iframe_url_when_insecure=None,
        video_iframe_url_when_secure=None,
        **kwargs
    ):

        self.video_iframe_height = video_iframe_height
        self.video_iframe_width = video_iframe_width
        self.video_iframe_host = video_iframe_host
        self.video_iframe_path = video_iframe_path
        self.video_iframe_supports_https = video_iframe_supports_https
        self.video_iframe_url_when_insecure = video_iframe_url_when_insecure
        self.video_iframe_url_when_secure = video_iframe_url_when_secure

        vars(self).update(kwargs)


class CustomField(CoreObject):

    def __init__(
        self,
        custom_field_data=None,
        custom_field_label=None,
        custom_field_name=None,
        **kwargs
    ):
        self.custom_field_data = custom_field_data
        self.custom_field_label = custom_field_label
        self.custom_field_name = custom_field_name

        vars(self).update(kwargs)


class CustomFilter(CoreObject):

    def __init__(
        self,
        custom_filter_desc=None,
        custom_filter_key=None,
        **kwargs
    ):
        self.custom_filter_desc = custom_filter_desc
        self.custom_filter_key = custom_filter_key

        vars(self).update(kwargs)


class Performance(CoreObject):

    def __init__(
        self,
        is_limited,
        perf_token=None,
        date_desc=None,
        date_utc_offset=None,
        date_utc_seconds=None,
        date_yyyymmdd=None,
        has_pool_seats=None,
        perf_is_visible=None,
        perf_subdata=None,
        perf_type_code=None,
        running_time=None,
        time_desc=None,
        time_hhmmss=None,
        perf_name=None,
        cost_range=None,
        cached_max_seats=None,
        **kwargs
    ):
        self.is_limited = is_limited
        self.perf_token = perf_token
        self.date_desc = date_desc
        self.date_utc_offset = date_utc_offset
        self.date_utc_seconds = date_utc_seconds
        self.date_yyyymmdd = date_yyyymmdd
        self.has_pool_seats = has_pool_seats
        self.perf_is_visible = perf_is_visible
        self.perf_subdata = perf_subdata
        self.perf_type_code = perf_type_code
        self.running_time = running_time
        self.time_desc = time_desc
        self.time_hhmmss = time_hhmmss
        self.perf_name = perf_name
        self.cost_range = cost_range
        self.cached_max_seats = cached_max_seats

        vars(self).update(kwargs)


class Month(CoreObject):

    def __init__(
        self,
        year_number,
        month_number,
        short_month_name,
        long_month_name,
        earliest_date,
        latest_date,
        **kwargs
    ):

        self.year_number = year_number
        self.month_number = month_number
        self.short_month_name = short_month_name
        self.long_month_name = long_month_name
        self.earliest_date = earliest_date
        self.latest_date = latest_date

        vars(self).update(kwargs)


class TicketType(CoreObject):

    def __init__(
        self,
        ticket_type_desc,
        price_bands,
        ticket_type_token=None,
        ticket_type_code=None,
        **kwargs
    ):
        self.ticket_type_desc = ticket_type_desc
        self.price_bands = price_bands
        self.ticket_type_token = ticket_type_token
        self.ticket_type_code = ticket_type_code

        vars(self).update(kwargs)


class PriceBand(CoreObject):

    def __init__(
        self,
        ticket_price,
        surcharge,
        number_available,
        is_offer,
        band_token,
        combined=None,
        seatprice=None,
        non_offer_combined=None,
        non_offer_seatprice=None,
        non_offer_surcharge=None,
        non_offer_ticket_price=None,
        percentage_saving=None,
        example_seats=None,
        price_band_code=None,
        price_band_desc=None,
        possible_discounts=None,
        example_seats_are_real=None,
        discount_code=None,
        discount_desc=None,
        discount_subdata=None,
        free_seat_blocks=None,
        raw_contiguous_seats=None,
        raw_total_seats=None,
        user_commission=None,
        gross_commission=None,
        **kwargs
    ):
        self.ticket_price = ticket_price
        self.surcharge = surcharge
        self.number_available = number_available
        self.is_offer = is_offer
        self.band_token = band_token
        self.combined = combined
        self.seatprice = seatprice
        self.non_offer_combined = non_offer_combined
        self.non_offer_seatprice = non_offer_seatprice
        self.non_offer_surcharge = non_offer_surcharge
        self.non_offer_ticket_price = non_offer_ticket_price
        self.percentage_saving = percentage_saving
        if example_seats is None:
            example_seats = []
        self.example_seats = example_seats
        self.price_band_code = price_band_code
        self.price_band_desc = price_band_desc
        self.possible_discounts = possible_discounts
        self.example_seats_are_real = example_seats_are_real
        self.discount_code = discount_code
        self.discount_desc = discount_desc
        self.discount_subdata = discount_subdata
        if free_seat_blocks is None:
            free_seat_blocks = []
        self.free_seat_blocks = free_seat_blocks
        self.raw_contiguous_seats = raw_contiguous_seats
        self.raw_total_seats = raw_total_seats
        self.user_commission = user_commission
        self.gross_commission = gross_commission

        vars(self).update(kwargs)


class Seat(CoreObject):

    def __init__(
        self,
        full_id=None,
        col_id=None,
        row_id=None,
        separator=None,
        is_restricted_view=None,
        seat_text=None,
        barcode=None,
        **kwargs
    ):
        self.full_id = full_id
        self.col_id = col_id
        self.row_id = row_id
        self.separator = separator
        self.is_restricted_view = is_restricted_view
        self.seat_text = seat_text
        self.barcode = barcode

        vars(self).update(kwargs)


class SeatBlock(CoreObject):

    def __init__(
        self,
        seat_block_token,
        block_length,
        seats=None,
        **kwargs
    ):
        self.seat_block_token = seat_block_token
        self.block_length = block_length
        if seats is None:
            seats = []
        self.seats = seats

        vars(self).update(kwargs)


class DespatchMethod(CoreObject):

    def __init__(
        self,
        despatch_type,
        despatch_desc,
        despatch_cost,
        despatch_token=None,
        despatch_code=None,
        **kwargs
    ):
        self.despatch_type = despatch_type
        self.despatch_desc = despatch_desc
        self.despatch_cost = despatch_cost
        self.despatch_token = despatch_token
        self.despatch_code = despatch_code

        vars(self).update(kwargs)


class Country(CoreObject):

    def __init__(
        self,
        country_code,
        country_desc,
        **kwargs
    ):
        self.country_code = country_code
        self.country_desc = country_desc

        vars(self).update(kwargs)


class Currency(CoreObject):

    def __init__(
        self,
        currency_code,
        currency_number,
        currency_pre_symbol,
        currency_post_symbol,
        currency_factor=None,
        currency_places=None,
        **kwargs
    ):
        self.currency_code = currency_code
        self.currency_number = currency_number
        self.currency_pre_symbol = currency_pre_symbol
        self.currency_post_symbol = currency_post_symbol
        self.currency_factor = currency_factor
        self.currency_places = currency_places

        vars(self).update(kwargs)


class Discount(CoreObject):

    def __init__(
        self,
        surcharge,
        ticket_price=None,
        discount_token=None,
        discount_type=None,
        discount_desc=None,
        discount_code=None,
        seatprice=None,
        no_of_tickets=None,
        seats=None,
        number_available=None,
        raw_contiguous_seats=None,
        raw_total_seats=None,
        user_commission=None,
        gross_commission=None,
        **kwargs
    ):
        self.discount_token = discount_token
        self.ticket_price = ticket_price
        self.surcharge = surcharge
        self.discount_type = discount_type
        self.discount_desc = discount_desc
        self.discount_code = discount_code
        self.seatprice = seatprice
        self.no_of_tickets = no_of_tickets
        if seats is None:
            seats = []
        self.seats = seats
        self.number_available = number_available
        self.raw_contiguous_seats = raw_contiguous_seats
        self.raw_total_seats = raw_total_seats
        self.user_commission = user_commission
        self.gross_commission = gross_commission

        vars(self).update(kwargs)


class Order(CoreObject):

    def __init__(
        self,
        item_number,
        venue_desc,
        event_desc,
        despatch_desc,
        ticket_type_desc,
        total_seatprice,
        total_surcharge,
        total_no_of_tickets,
        order_token=None,
        currency=None,
        despatch_method=None,
        discounts=None,
        performance=None,
        event=None,
        backend_purchase_reference=None,
        requested_seats=None,
        seat_request_status=None,
        user_commission=None,
        gross_commission=None,
        **kwargs
    ):
        self.item_number = item_number
        self.venue_desc = venue_desc
        self.event_desc = event_desc
        self.despatch_desc = despatch_desc
        self.ticket_type_desc = ticket_type_desc
        self.total_seatprice = total_seatprice
        self.total_surcharge = total_surcharge
        self.total_no_of_tickets = total_no_of_tickets
        self.order_token = order_token
        self.currency = currency
        self.despatch_method = despatch_method
        if discounts is None:
            discounts = []
        self.discounts = discounts
        self.performance = performance
        self.event = event
        self.backend_purchase_reference = backend_purchase_reference
        if requested_seats is None:
            requested_seats = []
        self.requested_seats = requested_seats
        self.seat_request_status = seat_request_status
        self.user_commission = user_commission
        self.gross_commission = gross_commission

        vars(self).update(kwargs)


class Trolley(CoreObject):

    def __init__(
        self,
        trolley_order_count,
        trolley_bundle_count,
        bundles=None,
        purchase_result=None,
        transaction_id=None,
        purchase_error=None,
        **kwargs
    ):
        self.trolley_order_count = trolley_order_count
        self.trolley_bundle_count = trolley_bundle_count
        if bundles is None:
            bundles = []
        self.bundles = bundles
        self.purchase_result = purchase_result
        self.transaction_id = transaction_id
        self.purchase_error = purchase_error

        vars(self).update(kwargs)


class Bundle(CoreObject):

    def __init__(
        self,
        bundle_source_desc,
        bundle_source_code,
        bundle_order_count,
        bundle_total_seatprice,
        bundle_total_surcharge,
        bundle_total_despatch,
        bundle_total_cost=None,
        orders=None,
        currency=None,
        purchase_result=None,
        debitor_choices=None,
        **kwargs
    ):
        self.bundle_source_desc = bundle_source_desc
        self.bundle_source_code = bundle_source_code
        self.bundle_order_count = bundle_order_count
        self.bundle_total_seatprice = bundle_total_seatprice
        self.bundle_total_surcharge = bundle_total_surcharge
        self.bundle_total_despatch = bundle_total_despatch
        self.bundle_total_cost = bundle_total_cost
        if orders is None:
            orders = []
        self.orders = orders
        self.currency = currency
        self.purchase_result = purchase_result
        self.debitor_choices = debitor_choices

        vars(self).update(kwargs)


class PurchaseResult(CoreObject):

    def __init__(
        self,
        success,
        failure_reason=None,
        is_semi_credit=None,
        is_partial=None,
        failed_cv_two=None,
        failed_avs=None,
        failed_3d_secure=None,
        **kwargs
    ):
        self.success = success
        self.failure_reason = failure_reason
        self.is_semi_credit = is_semi_credit
        self.is_partial = is_partial
        self.failed_cv_two = failed_cv_two
        self.failed_avs = failed_avs
        self.failed_3d_secure = failed_3d_secure

        vars(self).update(kwargs)


class CostRange(CoreObject):

    def __init__(
        self,
        currency,
        max_combined=None,
        max_surcharge=None,
        max_seatprice=None,
        min_combined=None,
        min_surcharge=None,
        min_seatprice=None,
        best_value_offer=None,
        max_saving_offer=None,
        top_price_offer=None,
        no_singles_cost_range=None,
        quantity_options=None,
        **kwargs
    ):
        self.max_combined = max_combined
        self.max_surcharge = max_surcharge
        self.min_combined = min_combined
        self.max_seatprice = max_seatprice
        self.min_seatprice = min_seatprice
        self.min_surcharge = min_surcharge
        self.best_value_offer = best_value_offer
        self.max_saving_offer = max_saving_offer
        self.top_price_offer = top_price_offer
        self.currency = currency
        self.no_singles_cost_range = no_singles_cost_range
        self.quantity_options = quantity_options

        vars(self).update(kwargs)


class Review(CoreObject):

    def __init__(
        self,
        is_user_review=None,
        review_date_desc=None,
        review_time_desc=None,
        review_date_yyyymmdd=None,
        review_time_hhmmss=None,
        review_title=None,
        review_body=None,
        review_author=None,
        review_lang=None,
        star_rating=None,
        **kwargs
    ):

        self.is_user_review = is_user_review
        self.review_date_desc = review_date_desc
        self.review_time_desc = review_time_desc
        self.review_date_yyyymmdd = review_date_yyyymmdd
        self.review_time_hhmmss = review_time_hhmmss
        self.review_title = review_title
        self.review_body = review_body
        self.review_author = review_author
        self.review_lang = review_lang
        self.star_rating = star_rating

        vars(self).update(kwargs)


class Customer(CoreObject):

    def __init__(
        self,
        first_name,
        first_name_latin,
        last_name,
        last_name_latin,
        town,
        town_latin,
        home_phone,
        work_phone,
        country_code,
        initials=None,
        initials_latin=None,
        suffix=None,
        suffix_latin=None,
        addr_line_one=None,
        addr_line_one_latin=None,
        addr_line_two=None,
        addr_line_two_latin=None,
        county=None,
        county_latin=None,
        postcode=None,
        postcode_latin=None,
        country=None,
        country_latin=None,
        title=None,
        title_latin=None,
        email_addr=None,
        dp_supplier=None,
        dp_user=None,
        dp_world=None,
        agent_ref=None,
        **kwargs
    ):

        self.first_name = first_name
        self.first_name_latin = first_name_latin
        self.initials = initials
        self.initials_latin = initials_latin
        self.last_name = last_name
        self.last_name_latin = last_name_latin
        self.suffix = suffix
        self.suffix_latin = suffix_latin
        self.addr_line_one = addr_line_one
        self.addr_line_one_latin = addr_line_one_latin
        self.addr_line_two = addr_line_two
        self.addr_line_two_latin = addr_line_two_latin
        self.town = town
        self.town_latin = town_latin
        self.county = county
        self.county_latin = county_latin
        self.postcode = postcode
        self.postcode_latin = postcode_latin
        self.country_code = country_code
        self.country = country
        self.country_latin = country_latin
        self.title = title
        self.title_latin = title_latin
        self.email_addr = email_addr
        self.home_phone = home_phone
        self.work_phone = work_phone
        self.dp_supplier = dp_supplier
        self.dp_user = dp_user
        self.dp_world = dp_world
        self.agent_ref = agent_ref

        vars(self).update(kwargs)


class SalePage(CoreObject):

    def __init__(
        self,
        sale_page_type,
        sale_page_subtype,
        sale_page,
        **kwargs
    ):

        self.sale_page_type = sale_page_type
        self.sale_page_subtype = sale_page_subtype
        self.sale_page = sale_page

        vars(self).update(kwargs)


class SelfPrintHTMLPage(CoreObject):

    def __init__(
        self,
        page_url,
        item_number,
        complete_page_url=None,
        **kwargs
    ):

        self.page_url = page_url
        self.item_number = item_number
        self.complete_page_url = complete_page_url

        vars(self).update(kwargs)


class Commission(CoreObject):

    def __init__(
        self,
        amount_excluding_vat,
        amount_including_vat,
        commission_currency,
        **kwargs
    ):

        self.amount_excluding_vat = amount_excluding_vat
        self.amount_including_vat = amount_including_vat
        self.commission_currency = commission_currency

        vars(self).update(kwargs)


class StructuredInfoItem(CoreObject):

    def __init__(
        self,
        key,
        name=None,
        value=None,
        **kwargs
    ):

        self.key = key
        self.name = name
        self.value = value

        vars(self).update(kwargs)


class AvailDetail(CoreObject):

    def __init__(
        self,
        avail_currency,
        seatprice,
        surcharge,
        full_seatprice=None,
        full_surcharge=None,
        absolute_saving=None,
        percentage_saving=None,
        day_mask=None,
        available_dates=None,
        **kwargs
    ):

        self.currency = avail_currency
        self.seatprice = seatprice
        self.surcharge = surcharge
        self.full_seatprice = full_seatprice
        self.full_surcharge = full_surcharge
        self.absolute_saving = absolute_saving
        self.percentage_saving = percentage_saving
        self.day_mask = day_mask
        self.available_dates = available_dates

        vars(self).update(kwargs)
