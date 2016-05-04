# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from . import api_exceptions as aex
from . import core_objects as objects
from .util import create_dict_from_xml_element


def script_error(root):

    if root.tag == 'script_error':
        raise aex.APIException(
            call=root.tag,
            code=root.findtext('error_code'),
            description=root.findtext('error_desc')
        )
    else:
        return root


def error_check(root):
    fail_code = root.findtext('fail_code')

    if fail_code is not None:

        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    else:
        return root


def _text_dict(elem):
    return dict((e.tag, e.text) for e in list(elem))


def _parse_running_user(running_user_elem):
    return objects.RunningUser(**_text_dict(running_user_elem))


def start_session_resolve_user_result(root):
    root = error_check(root)

    ret_dict = {
        'crypto_block': root.findtext('crypto_block'),
        'country_code': root.findtext('country_code'),
        'country_desc': root.findtext('country_desc'),
    }

    running_user = root.find('running_user')

    if running_user is not None:
        ret_dict['running_user'] = _parse_running_user(running_user)

    return ret_dict


def style_map_result(root):
    root = error_check(root)

    ret_dict = {
        'mapping': []
    }

    for m in root.findall('mapping'):
        ret_dict['mapping'].append(_text_dict(m))

    return ret_dict


def _parse_geo_data(geo_elem):
    return objects.GeoData(**_text_dict(geo_elem))


def _parse_subclass(sub_elem):
    return objects.SubClass(**_text_dict(sub_elem))


def _parse_class(class_elem):
    subclasses = []
    for s in class_elem.findall('subclass'):
        subclasses.append(_parse_subclass(s))
        class_elem.remove(s)

    c_arg = _text_dict(class_elem)
    if subclasses:
        c_arg['subclasses'] = subclasses

    return objects.Class(**c_arg)


def _parse_event_media(event_media_elem):
    return objects.EventMedia(**_text_dict(event_media_elem))


def _parse_cost_range(cost_range_elem):
    add_arg = {}

    currency = cost_range_elem.find('range_currency')

    if currency is not None:
        add_arg['currency'] = _parse_currency(currency)
        cost_range_elem.remove(currency)

    no_singles = cost_range_elem.find('no_singles_cost_range')

    if no_singles is not None:
        add_arg['no_singles_cost_range'] = _parse_cost_range(no_singles)
        cost_range_elem.remove(no_singles)

    cr_arg = create_dict_from_xml_element(cost_range_elem)
    cr_arg.update(add_arg)

    return objects.CostRange(**cr_arg)


def _parse_review(review_elem):
    return objects.Review(**_text_dict(review_elem))


def _parse_video_iframe(video_iframe_elem):
    return objects.VideoIframe(**_text_dict(video_iframe_elem))


def _parse_custom_field(custom_field_elem):
    return objects.CustomField(**_text_dict(custom_field_elem))


def _parse_custom_filter(custom_filter_elem):
    return objects.CustomFilter(**_text_dict(custom_filter_elem))


def _parse_structured_info(structured_info_elem):

    ret_dict = {}

    for elem in structured_info_elem:

        si_args = _text_dict(elem)
        si_args['key'] = elem.tag

        ret_dict[elem.tag] = objects.StructuredInfoItem(
            **si_args
        )

    return ret_dict


def _parse_avail_detail(avail_detail_elem):

    ad_args = {}

    currency = avail_detail_elem.find('avail_currency')

    if currency is not None:
        ad_args['avail_currency'] = _parse_currency(currency)
        avail_detail_elem.remove(currency)

    ad_args.update(create_dict_from_xml_element(avail_detail_elem))
    return objects.AvailDetail(**ad_args)


def _parse_avail_details(avail_details_elem):
    """Parse the avail_details element. Does not make use of core TicketType
    or PriceBand since we only use a very limited subset of their data
    """

    ticket_types = []

    for tt in avail_details_elem.findall('ticket_type'):
        price_bands = []

        for pb in tt.findall('price_band'):
            avail_detail_list = []

            for ad in pb.findall('avail_detail'):
                avail_detail_list.append(_parse_avail_detail(ad))

            price_bands.append({
                'price_band_code': pb.findtext('price_band_code'),
                'price_band_desc': pb.findtext('price_band_desc'),
                'avail_details': avail_detail_list,
            })

        ticket_types.append({
            'ticket_type_code': tt.findtext('ticket_type_code'),
            'ticket_type_desc': tt.findtext('ticket_type_desc'),
            'price_bands': price_bands,
        })

    return {'ticket_types': ticket_types}


def _parse_event(event_elem):

    objs = {}

    classes = []
    for c in event_elem.findall('class'):

        classes.append(_parse_class(c))
        event_elem.remove(c)

    objs['classes'] = classes

    event_medias = []
    for event_media in event_elem.findall('event_media'):
        event_medias.append(_parse_event_media(event_media))
        event_elem.remove(event_media)

    objs['event_medias'] = event_medias

    reviews = event_elem.find('reviews')

    if reviews is not None:
        review_list = []

        for review in reviews.findall('review'):
            review_list.append(_parse_review(review))

        event_elem.remove(reviews)
        objs['reviews'] = review_list

    geo_elem = event_elem.find('geo_data')

    if geo_elem is not None:
        objs['geo_data'] = _parse_geo_data(geo_elem)
        event_elem.remove(geo_elem)

    cost_range = event_elem.find('cost_range')

    if cost_range is not None:
        objs['cost_range'] = _parse_cost_range(cost_range)
        event_elem.remove(cost_range)

    custom_fields = []

    for custom_field in event_elem.findall('custom_field'):
        custom_fields.append(_parse_custom_field(custom_field))
        event_elem.remove(custom_field)

    objs['custom_fields'] = custom_fields

    custom_filters = []

    for custom_filter in event_elem.findall('custom_filter'):
        custom_filters.append(_parse_custom_filter(custom_filter))
        event_elem.remove(custom_filter)

    objs['custom_filters'] = custom_filters

    video_iframe = event_elem.find('video_iframe')

    if video_iframe is not None:
        objs['video_iframe'] = _parse_video_iframe(video_iframe)
        event_elem.remove(video_iframe)

    structured_info = event_elem.find('structured_info')

    if structured_info is not None:
        objs['structured_info'] = _parse_structured_info(structured_info)
        event_elem.remove(structured_info)

    avail_details = event_elem.find('avail_details')

    if avail_details is not None:
        objs['avail_details'] = _parse_avail_details(avail_details)
        event_elem.remove(avail_details)

    component_events = event_elem.find('meta_event_component_events')
    if component_events is not None:
        component_events_list = []
        for event in component_events.findall('event'):
            component_events_list.append(_parse_event(event))
            component_events.remove(event)
        objs['component_events'] = component_events_list

    e_arg = create_dict_from_xml_element(event_elem)
    e_arg.update(objs)

    return objects.Event(**e_arg)


def event_search_result(root):
    root = error_check(root)

    ret_dict = {
        'crypto_block': root.findtext('crypto_block'),
        'event': []
    }

    for e in root.findall('event'):
        ret_dict['event'].append(_parse_event(e))

    return ret_dict


def extra_info_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code in (
        '102', '103',
    ):
        raise aex.InvalidToken(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    event = _parse_event(root)

    return event


def _parse_performance(perf_elem):

    objs = {}

    cost_range = perf_elem.find('cost_range')

    if cost_range is not None:
        objs['cost_range'] = _parse_cost_range(cost_range)
        perf_elem.remove(cost_range)

    p_arg = create_dict_from_xml_element(perf_elem)
    p_arg.update(objs)

    return objects.Performance(**p_arg)


def date_time_options_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code in (
        '202', '203'
    ):
        raise aex.InvalidToken(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    ret_dict = {
        'crypto_block': root.findtext('crypto_block'),
        'need_departure_date': root.findtext('need_departure_date'),
        'has_perf_names': root.findtext('has_perf_names'),
    }

    using_perf_list = root.find('using_perf_list')
    using_usage_date = root.find('using_usage_date')

    if using_perf_list is not None:
        perf_list = []
        for p in using_perf_list.findall('performance'):
            perf_list.append(_parse_performance(p))

        ret_dict['using_perf_list'] = {'performances': perf_list}

    elif using_usage_date is not None:
        ret_dict['using_usage_date'] = create_dict_from_xml_element(
            using_usage_date
        )

    return ret_dict


def _parse_month(month_elem):
    return objects.Month(**_text_dict(month_elem))


def month_options_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code in (
        '202', '203'
    ):
        raise aex.InvalidToken(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    ret_dict = {
        'need_departure_date': root.findtext('need_departure_date'),
        'has_perf_names': root.findtext('has_perf_names'),
    }

    using_perf_list = root.find('using_perf_list')

    if using_perf_list is not None:
        month_list = []
        for m in using_perf_list.findall('month'):
            month_list.append(_parse_month(m))

        ret_dict['months'] = month_list

    return ret_dict


def _parse_country(country_elem):
    return objects.Country(**_text_dict(country_elem))


def _parse_currency(curr_elem):
    return objects.Currency(**_text_dict(curr_elem))


def _parse_despatch_method(desp_elem):

    d_arg = _text_dict(desp_elem)

    permitted_countries = desp_elem.find('permitted_countries')

    if permitted_countries is not None:
        country = []
        for c in permitted_countries.findall('country'):
            country.append(_parse_country(c))

        d_arg['permitted_countries'] = {'country': country}

    return objects.DespatchMethod(**d_arg)


def _parse_seats(seats_elem):

    seats = []

    for s in seats_elem.findall('id_details'):
        seats.append(objects.Seat(**_text_dict(s)))

    return seats


def _parse_seat_block(seat_block_elem):

    sb_arg = {}

    seats = []

    for s in seat_block_elem.findall('id_details'):
        seats.append(objects.Seat(**_text_dict(s)))
        seat_block_elem.remove(s)

    sb_arg = _text_dict(seat_block_elem)

    if seats:
        sb_arg['seats'] = seats

    return objects.SeatBlock(**sb_arg)


def _parse_free_seat_blocks(free_seat_blocks_elem):

    seat_blocks = []

    for sb in free_seat_blocks_elem.findall('seat_block'):
        seat_blocks.append(_parse_seat_block(sb))

    return seat_blocks


def _parse_commission(commission_elem):

    c_args = {}

    currency = commission_elem.find('commission_currency')

    if currency is not None:
        c_args['commission_currency'] = _parse_currency(currency)
        commission_elem.remove(currency)

    c_args.update(_text_dict(commission_elem))

    return objects.Commission(**c_args)


def _parse_price_band(price_elem):

    objs = {}

    possible_discounts = price_elem.find('possible_discounts')

    if possible_discounts is not None:
        discounts_list = []
        for d in possible_discounts.findall('discount'):
            discounts_list.append(_parse_discount(d))

        objs['possible_discounts'] = discounts_list
        price_elem.remove(possible_discounts)

    example_seats = price_elem.find('example_seats')

    if example_seats is not None:
        objs['example_seats'] = _parse_seats(example_seats)
        price_elem.remove(example_seats)

    free_seat_blocks = price_elem.find('free_seat_blocks')

    if free_seat_blocks is not None:
        objs['free_seat_blocks'] = _parse_free_seat_blocks(
            free_seat_blocks
        )
        price_elem.remove(free_seat_blocks)

    user_commission = price_elem.find('user_commission')
    if user_commission is not None:
        objs['user_commission'] = _parse_commission(
            user_commission
        )
        price_elem.remove(user_commission)

    gross_commission = price_elem.find('gross_commission')
    if gross_commission is not None:
        objs['gross_commission'] = _parse_commission(
            gross_commission
        )
        price_elem.remove(gross_commission)

    p_arg = _text_dict(price_elem)
    p_arg.update(objs)

    return objects.PriceBand(**p_arg)


def _parse_ticket_type(tt_elem):

    price_bands = []

    for p in tt_elem.findall('price_band'):
        price_bands.append(_parse_price_band(p))
        tt_elem.remove(p)

    t_arg = _text_dict(tt_elem)

    t_arg['price_bands'] = price_bands

    return objects.TicketType(**t_arg)


def availability_options_result(root):
    root = error_check(root)

    backend_call_failed = root.find('backend_call_failed')

    if backend_call_failed:
        raise aex.BackendCallFailure(call=root.tag)

    ret_dict = {
        'crypto_block': root.findtext('crypto_block')
    }

    quantity_options = root.find('quantity_options')

    if quantity_options is not None:
        ret_dict['quantity_options'] = create_dict_from_xml_element(
            quantity_options
        )

    availability = root.find('availability')

    if availability is not None:

        ticket_types = []
        for t in availability.findall('ticket_type'):

            ticket_types.append(_parse_ticket_type(t))

        ret_dict['ticket_type'] = ticket_types

    despatch_options = root.find('despatch_options')

    if despatch_options is not None:
        despatch_method = []
        for d in despatch_options.findall('despatch_method'):

            despatch_method.append(_parse_despatch_method(d))

        ret_dict['despatch_options'] = {'despatch_method': despatch_method}

    currency = root.find('currency')

    if currency is not None:
        ret_dict['currency'] = _parse_currency(currency)

    event = root.find('event')

    if event is not None:
        ret_dict['event'] = _parse_event(event)

    performance = root.find('performance')

    if performance is not None:
        ret_dict['performance'] = _parse_performance(performance)

    return ret_dict


def despatch_options_result(root):
    root = error_check(root)

    ret_dict = {}

    despatch_options = root.find('despatch_options')

    if despatch_options is not None:
        despatch_method = []
        for d in despatch_options.findall('despatch_method'):

            despatch_method.append(_parse_despatch_method(d))

        ret_dict['despatch_options'] = {'despatch_method': despatch_method}

    currency = root.find('currency')

    if currency is not None:
        ret_dict['currency'] = _parse_currency(currency)

    event = root.find('event')

    if event is not None:
        ret_dict['event'] = _parse_event(event)

    performance = root.find('performance')

    if performance is not None:
        ret_dict['performance'] = _parse_performance(performance)

    return ret_dict


def _parse_discount(discount_elem):

    d_arg = _text_dict(discount_elem)

    seats = discount_elem.find('seats')

    if seats is not None:
        d_arg['seats'] = _parse_seats(seats)

    user_commission = discount_elem.find('user_commission')
    if user_commission is not None:
        d_arg['user_commission'] = _parse_commission(
            user_commission
        )

    gross_commission = discount_elem.find('gross_commission')
    if gross_commission is not None:
        d_arg['gross_commission'] = _parse_commission(
            gross_commission
        )

    return objects.Discount(**d_arg)


def discount_options_result(root):
    root = error_check(root)

    backend_call_failed = root.find('backend_call_failed')

    if backend_call_failed:
        raise aex.BackendCallFailure(call=root.tag)

    ret_dict = {
        'crypto_block': root.findtext('crypto_block')
    }

    blanket_discount_only = root.findtext('blanket_discount_only')

    if blanket_discount_only is not None:
        ret_dict['blanket_discount_only'] = blanket_discount_only

    currency = root.find('currency')

    if currency is not None:
        ret_dict['currency'] = _parse_currency(currency)

    discount_limit = root.findtext('discount_limit')

    if discount_limit is not None:
        ret_dict['discount_limit'] = discount_limit

    discounts_list = []
    for td in root.findall('discounts'):
        discount_objs = []
        for d in td.findall('discount'):
            discount_objs.append(_parse_discount(d))

        discounts_list.append(discount_objs)

    ret_dict['discounts'] = discounts_list

    return ret_dict


def _parse_order(order_elem):

    objs = {}

    despatch_method = order_elem.find('despatch_method')

    if despatch_method is not None:
        objs['despatch_method'] = _parse_despatch_method(despatch_method)
        order_elem.remove(despatch_method)

    discounts_list = []
    for discount in order_elem.findall('discount'):
        discounts_list.append(_parse_discount(discount))
        order_elem.remove(discount)

    objs['discounts'] = discounts_list

    performance = order_elem.find('performance')

    if performance is not None:
        objs['performance'] = _parse_performance(performance)
        order_elem.remove(performance)

    event = order_elem.find('event')

    if event is not None:
        objs['event'] = _parse_event(event)
        order_elem.remove(event)

    requested_seats = order_elem.find('requested_seats')

    if requested_seats is not None:
        objs['requested_seats'] = _parse_seats(requested_seats)
        order_elem.remove(requested_seats)

    user_commission = order_elem.find('user_commission')
    if user_commission is not None:
        objs['user_commission'] = _parse_commission(
            user_commission
        )
        order_elem.remove(user_commission)

    gross_commission = order_elem.find('gross_commission')
    if gross_commission is not None:
        objs['gross_commission'] = _parse_commission(
            gross_commission
        )
        order_elem.remove(gross_commission)

    o_arg = _text_dict(order_elem)
    o_arg.update(objs)

    return objects.Order(**o_arg)


def create_order_result(root):
    root = error_check(root)

    ret_dict = {
        'crypto_block': root.findtext('crypto_block')
    }

    order = root.find('order')

    if order is not None:
        ret_dict['order'] = _parse_order(order)

    ret_dict['order_token'] = root.findtext('order_token')

    currency = root.find('currency')

    if currency is not None:
        ret_dict['currency'] = _parse_currency(currency)

    return ret_dict


def create_order_and_reserve_result(root):
    return make_reservation_result(root)


def trolley_add_order_result(root):
    root = error_check(root)

    ret_dict = {
        'crypto_block': root.findtext('crypto_block'),
        'add_possible': root.findtext('add_possible'),
        'trolley_token': root.findtext('trolley_token'),
        'trolley_order_count': root.findtext('trolley_order_count'),
        'added_item_number': root.findtext('added_item_number'),
    }

    if ret_dict['add_possible'] == 'no':
        errors = []

        if root.findtext('trolley_bad_bundle') == 'yes':
            errors.append(
                aex.TrolleyAddBadBundle(
                    root.findtext('trolley_bad_bundle_max_size')
                )
            )

        if root.findtext('trolley_bad_combo') == 'yes':
            errors.append(
                aex.TrolleyAddBadCombo(
                    system=root.findtext('trolley_bad_combo_system'),
                    system_desc=root.findtext('trolley_bad_combo_system_desc')
                )
            )

        if root.findtext('trolley_bad_card_types') == 'yes':
            errors.append(aex.TrolleyAddBadCardTypes())

        if root.findtext('trolley_bad_countries') == 'yes':
            errors.append(aex.TrolleyAddBadCountries())

        if root.findtext('trolley_bad_currency_mix') == 'yes':

            curr_elem = root.find('trolley_bad_currency')
            if curr_elem:
                currency = _parse_currency(curr_elem)
            else:
                currency = None

            errors.append(
                aex.TrolleyAddBadCurrencyMix(
                    system=root.findtext(
                        'trolley_bad_currency_system'
                    ),
                    system_desc=root.findtext(
                        'trolley_bad_currency_system_desc'
                    ),
                    currency=currency,
                    currency_name=root.findtext(
                        'trolley_bad_currency_name'
                    )
                )
            )

        if root.findtext('trolley_bad_depart') == 'yes':
            errors.append(aex.TrolleyAddBadDepart())

        if root.findtext('trolley_bad_send') == 'yes':
            errors.append(aex.TrolleyAddBadSend())

        if errors:
            raise aex.TrolleyAddErrors(errors)

    trolley = root.find('trolley')

    if trolley is not None:
        ret_dict['trolley'] = _parse_trolley(trolley)

    return ret_dict


def _parse_trolley(trolley_elem):

    objs = {}

    purchase_result = trolley_elem.find('purchase_result')

    if purchase_result is not None:
        objs['purchase_result'] = _parse_purchase_result(purchase_result)
        trolley_elem.remove(purchase_result)

    bundles = []

    for bundle in trolley_elem.findall('bundle'):

        bundles.append(_parse_bundle(bundle))
        trolley_elem.remove(bundle)

    objs['bundles'] = bundles

    t_arg = _text_dict(trolley_elem)
    t_arg.update(objs)

    return objects.Trolley(**t_arg)


def _parse_purchase_result(purchase_result_elem):
    return objects.PurchaseResult(**_text_dict(purchase_result_elem))


def _parse_debitor_choices(elem):
    debitor_elems = elem.findall('debitor')
    return [create_dict_from_xml_element(choice) for choice in debitor_elems]


def _parse_bundle(bundle_elem):

    objs = {}

    purchase_result = bundle_elem.find('purchase_result')

    if purchase_result is not None:
        objs['purchase_result'] = _parse_purchase_result(purchase_result)
        bundle_elem.remove(purchase_result)

    currency = bundle_elem.find('currency')

    if currency is not None:
        objs['currency'] = _parse_currency(currency)
        bundle_elem.remove(currency)

    orders = []

    for order in bundle_elem.findall('order'):
        orders.append(_parse_order(order))
        bundle_elem.remove(order)

    objs['orders'] = orders

    objs['debitor_choices'] = []

    debitor_choices = bundle_elem.find('debitor_choices')
    if debitor_choices:
        objs['debitor_choices'] = _parse_debitor_choices(debitor_choices)

    b_arg = _text_dict(bundle_elem)
    b_arg.update(objs)

    return objects.Bundle(**b_arg)


def trolley_describe_result(root):
    root = error_check(root)

    trolley = root.find('trolley')

    ret_dict = {
        'trolley': _parse_trolley(trolley)
    }

    return ret_dict


def trolley_remove_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code == '803':
        raise aex.TrolleyPurchased(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '804':
        raise aex.TrolleyReserved(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    ret_dict = {
        'crypto_block': root.findtext('crypto_block'),
        'trolley_token': root.findtext('trolley_token'),
        'trolley_order_count': root.findtext('trolley_order_count'),
    }

    trolley = root.find('trolley')

    if trolley is not None:
        ret_dict['trolley'] = _parse_trolley(trolley)

    return ret_dict


def make_reservation_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code == '903':
        raise aex.TrolleyPurchased(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '904':
        raise aex.TrolleyReserved(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    objs = {}

    trolley = root.find('trolley')

    if trolley is not None:
        objs['trolley'] = _parse_trolley(trolley)
        root.remove(trolley)

    failed_orders = root.find('failed_orders')

    if failed_orders is not None:
        failed_list = []
        for order in failed_orders.findall('order'):
            failed_list.append(_parse_order(order))
            failed_orders.remove(order)

        objs['failed_orders'] = failed_list
        root.remove(failed_orders)

    ret_dict = create_dict_from_xml_element(root)
    ret_dict.update(objs)

    avail_test = [
        x for x in ret_dict.keys() if x not in (
            'subdomain_user_is_bad', 'currency'
        )
    ]

    if not avail_test:
        raise aex.NoAvailability(
            call=root.tag
        )

    return ret_dict


def get_reservation_link_result(root):
    root = error_check(root)

    return create_dict_from_xml_element(root)


def release_reservation_result(root):
    root = error_check(root)

    return create_dict_from_xml_element(root)


def purchase_reservation_part_one_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code == '1301':
        raise aex.ReservationExpired(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1306':
        raise aex.InvalidCountryForDespatch(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1307':
        raise aex.InvalidEmailAddress(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1308':
        raise aex.IncompleteCustomerDetails(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1309':
        raise aex.NoCardNumberProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1310':
        raise aex.UnknownCardType(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1311':
        raise aex.InvalidCardType(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1312':
        raise aex.InvalidCardNumber(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1313':
        raise aex.NoExpiryDateProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1314':
        raise aex.InvalidExpiryDate(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1315':
        raise aex.NoCV2Provided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1316':
        raise aex.InvalidCV2(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1317':
        raise aex.NoIssueNumberProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1319':
        raise aex.InvalidIssueNumber(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1321':
        raise aex.IncompleteAltBillingAddress(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1322':
        raise aex.NoStartDateProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1323':
        raise aex.InvalidStartDate(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    return create_dict_from_xml_element(root)


def _parse_customer(customer_elem):
    return objects.Customer(**_text_dict(customer_elem))


def _parse_self_print_html_page(self_print_html_page_elem):
    return objects.SelfPrintHTMLPage(**_text_dict(self_print_html_page_elem))


def purchase_reservation_part_two_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code == '1404':
        raise aex.ReservationExpired(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    failed_cv_two = root.findtext('failed_cv_two')
    failed_avs = root.findtext('failed_avs')
    failed_3d_secure = root.findtext('failed_3d_secure')
    purchase_fail_code = root.findtext('purchase_fail_code')

    if purchase_fail_code == '1':
        raise aex.FraudTriggered(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code in ('2', '3'):
        raise aex.CardAuthorisationFailed(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '4':
        raise aex.ReservationAlreadyPurchased(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '5':
        raise aex.PurchasePreviouslyAttempted(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '6':
        raise aex.PurchaseRefused(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '7':
        raise aex.PurchaseFailed(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code:
        raise aex.PurchaseException(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )

    objs = {}

    self_print_html_pages = []

    for self_print_html_page in root.findall('self_print_html_page'):

        self_print_html_pages.append(
            _parse_self_print_html_page(self_print_html_page)
        )
        root.remove(self_print_html_page)

    objs['self_print_html_pages'] = self_print_html_pages

    trolley = root.find('trolley')

    if trolley is not None:
        objs['trolley'] = _parse_trolley(trolley)
        root.remove(trolley)

    customer = root.find('customer')

    if customer is not None:
        objs['customer'] = _parse_customer(customer)
        root.remove(customer)

    ret_dict = create_dict_from_xml_element(root)
    ret_dict.update(objs)

    return ret_dict


def purchase_reservation(root):
    fail_code = root.findtext('fail_code')

    if fail_code == '1101':
        raise aex.ReservationExpired(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1106':
        raise aex.InvalidCountryForDespatch(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1107':
        raise aex.InvalidEmailAddress(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1108':
        raise aex.IncompleteCustomerDetails(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1109':
        raise aex.NoCardNumberProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1110':
        raise aex.UnknownCardType(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1111':
        raise aex.InvalidCardType(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1112':
        raise aex.InvalidCardNumber(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1113':
        raise aex.NoExpiryDateProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1114':
        raise aex.InvalidExpiryDate(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1115':
        raise aex.NoCV2Provided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1116':
        raise aex.InvalidCV2(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1117':
        raise aex.NoIssueNumberProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1119':
        raise aex.InvalidIssueNumber(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1121':
        raise aex.IncompleteAltBillingAddress(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1122':
        raise aex.NoStartDateProvided(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code == '1123':
        raise aex.InvalidStartDate(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    failed_cv_two = root.findtext('failed_cv_two')
    failed_avs = root.findtext('failed_avs')
    failed_3d_secure = root.findtext('failed_3d_secure')
    purchase_fail_code = root.findtext('purchase_fail_code')

    if purchase_fail_code == '1':
        raise aex.FraudTriggered(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code in ('2', '3'):
        raise aex.CardAuthorisationFailed(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '4':
        raise aex.ReservationAlreadyPurchased(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '5':
        raise aex.PurchasePreviouslyAttempted(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '6':
        raise aex.PurchaseRefused(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code == '7':
        raise aex.PurchaseFailed(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )
    elif purchase_fail_code:
        raise aex.PurchaseException(
            call=root.tag,
            code=purchase_fail_code,
            description=root.findtext('purchase_fail_desc'),
            failed_cv_two=failed_cv_two,
            failed_avs=failed_avs,
            failed_3d_secure=failed_3d_secure,
        )

    objs = {}

    self_print_html_pages = []

    for self_print_html_page in root.findall('self_print_html_page'):

        self_print_html_pages.append(
            _parse_self_print_html_page(self_print_html_page)
        )
        root.remove(self_print_html_page)

    objs['self_print_html_pages'] = self_print_html_pages

    trolley = root.find('trolley')

    if trolley is not None:
        objs['trolley'] = _parse_trolley(trolley)
        root.remove(trolley)

    customer = root.find('customer')

    if customer is not None:
        objs['customer'] = _parse_customer(customer)
        root.remove(customer)

    ret_dict = create_dict_from_xml_element(root)
    ret_dict.update(objs)

    return ret_dict


def _parse_sale_page(sale_page_elem):
    return objects.SalePage(**_text_dict(sale_page_elem))


def transaction_info_result(root):
    fail_code = root.findtext('fail_code')

    if fail_code in ('1201', '1202'):
        raise aex.InvalidToken(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )
    elif fail_code:
        raise aex.APIException(
            call=root.tag,
            code=fail_code,
            description=root.findtext('fail_desc')
        )

    ret_dict = {
        'transaction_status': root.findtext('transaction_status'),
        'minutes_left_on_reserve': root.findtext('minutes_left_on_reserve'),
        'language_list': root.findtext('language_list'),
        'remote_site': root.findtext('remote_site'),
    }

    objs = {}

    self_print_html_pages = []

    for self_print_html_page in root.findall('self_print_html_page'):

        self_print_html_pages.append(
            _parse_self_print_html_page(self_print_html_page)
        )
        root.remove(self_print_html_page)

    objs['self_print_html_pages'] = self_print_html_pages

    trolley = root.find('trolley')

    if trolley is not None:
        objs['trolley'] = _parse_trolley(trolley)
        root.remove(trolley)

    customer = root.find('customer')

    if customer is not None:
        objs['customer'] = _parse_customer(customer)
        root.remove(customer)

    external_sale_page = root.find('external_sale_page')

    if external_sale_page is not None:
        if len(list(external_sale_page)) > 0:
            objs['sale_page'] = _parse_sale_page(external_sale_page)
            root.remove(external_sale_page)

    ret_dict.update(objs)

    return ret_dict


def save_external_sale_page_result(root):
    root = error_check(root)

    return create_dict_from_xml_element(root)
