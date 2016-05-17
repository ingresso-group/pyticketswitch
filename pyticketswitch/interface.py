# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import logging
from datetime import datetime

import requests
import six

from . import parse, settings
from .api_exceptions import CommsException, InvalidResponse
from .util import create_xml_from_dict, dict_ignore_nones

try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml


logger = logging.getLogger(__name__)
filelog = logging.getLogger('filelog.' + __name__)


class CoreAPI(object):

    def __init__(
            self, username, password, url,
            remote_ip, remote_site, accept_language,
            api_request_timeout,
            sub_id=None,
            additional_elements=None,
            requests_session=None, custom_start_session=None):

        self.username = username
        self.password = password
        self.sub_id = sub_id

        self.url = url
        self.remote_ip = remote_ip
        self.remote_site = remote_site
        self.accept_language = accept_language
        self.content_language = None
        self.running_user = None
        self.custom_start_session = custom_start_session

        if api_request_timeout:
            self.api_request_timeout = api_request_timeout
        else:
            self.api_request_timeout = settings.API_REQUEST_TIMEOUT

        if not additional_elements:
            additional_elements = {}
        self.additional_elements = additional_elements

        # If no Requests session create a new one
        if not requests_session:
            requests_session = requests.Session()
        self.requests_session = requests_session

    def _post(self, method_name, data, url, headers=None):

        filelog.debug(
            u'URL=%s; API_REQUEST=%s',
            url, six.text_type(data, 'UTF-8')
        )

        response_string = None

        before = datetime.now()
        after = None

        try:
            response = self.requests_session.post(
                url=url, data=data, headers=headers,
                timeout=self.api_request_timeout,
            )
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            after = datetime.now()
            raise CommsException(
                underlying_exception=e,
                description=(
                    'HTTPError, message={0}'.format(
                        getattr(e, 'message', None),
                    )
                )
            )

        except requests.exceptions.Timeout as e:
            after = datetime.now()
            raise CommsException(
                underlying_exception=e,
                description=(
                    'Timeout, message={0}'.format(
                        getattr(e, 'message', None),
                    )
                )
            )

        except requests.exceptions.ConnectionError as e:
            after = datetime.now()
            raise CommsException(
                underlying_exception=e,
                description=(
                    'ConnectionError, message={0}'.format(
                        getattr(e, 'message', None),
                    )
                )
            )

        except requests.exceptions.RequestException as e:
            after = datetime.now()
            raise CommsException(
                underlying_exception=e,
                description=(
                    'RequestException, message={0}'.format(
                        getattr(e, 'message', None),
                    )
                )
            )

        else:
            after = datetime.now()
            response_string = response.content
            self.content_language = response.headers.get(
                'Content-Language')

            filelog.debug(
                u'API_RESPONSE=%s',
                six.text_type(response_string, 'UTF-8')
            )

        finally:
            if after:
                time_taken = (after - before).total_seconds()
                logger.debug(
                    'url=%s, api_call=%s, time_taken=%s',
                    url, method_name, time_taken
                )
            else:
                logger.error(
                    (
                        'Response time unknown, url=%s, ' +
                        'api_call=%s, request_time=%s'
                    ),
                    url, method_name, before.strftime('%d/%m/%Y %H:%M:%S')
                )

        return response_string

    def _create_xml_and_post(self, method_name, arg_dict, url=None):
        data = xml.tostring(
            create_xml_from_dict(method_name, arg_dict),
            encoding=b'UTF-8'
        )

        if not url:
            url = self.url

        headers = {
            'Content-Type': 'text/xml',
        }

        if self.accept_language:
            headers['Accept-Language'] = self.accept_language

        try:
            response = xml.fromstring(
                self._post(
                    method_name=method_name,
                    data=data,
                    headers=headers,
                    url=url
                )
            )
        except CommsException as e:
            logger.error(e)
            raise e

        except xml.ParseError as e:

            err_string = 'XML parsing error, detail="{0}", arguments="{1}"'

            raise InvalidResponse(
                underlying_exception=e,
                description=err_string.format(
                    str(e), arg_dict
                ),
            )

        return response

    def make_core_request(self, api_call, **kwargs):

        args = {
            'user_id': self.username,
            'sub_id': self.sub_id,
            'remote_ip': self.remote_ip,
            'remote_site': self.remote_site,
        }

        args.update(self.additional_elements)

        args.update(kwargs)

        return self._create_xml_and_post(
            method_name=api_call,
            arg_dict=dict_ignore_nones(**args),
            url=self.url
        )

    def parse_response(self, parse_function, xml_elem):
        """
        Calls the specified parse function
        """
        result = parse_function(
            parse.script_error(xml_elem)
        )
        return result

    def start_session(self):
        """
        Attempts to start a new user session with the creditials provided.
        If a custom start session method is provided then it will use that
        instead.
        The expected result from a custom_start_session method is a dictionary
        containing a crypto_block, and a running_user
        (pyticketswitch.core_objects.RunningUser)
        """

        if self.custom_start_session:
            resp = self.custom_start_session(
                remote_ip=self.remote_ip,
                remote_site=self.remote_site,
            )
            crypto_block = resp['crypto_block']
            self.running_user = resp['running_user']
            self.username = resp['running_user'].user_id
        else:
            arg_dict={
                'user_id': self.username,
                'user_passwd': self.password,
            }

            if self.sub_id:
                arg_dict.update(
                    sub_id=self.sub_id,
                )

            resp = self._create_xml_and_post(
                method_name='start_session',
                arg_dict=arg_dict,
            )

            parse.script_error(resp)
            running_user = resp.find('running_user')

            if running_user is not None:
                self.running_user = parse._parse_running_user(running_user)

            crypto_block = resp.findtext('crypto_block')

        return crypto_block

    def style_map(self, map_key):
        resp = self.make_core_request(
            'style_map',
            user_passwd=self.password,
            map_key=map_key
        )

        return self.parse_response(parse.style_map_result, resp)

    def event_search(
            self, crypto_block=None, upfront_data_token=None, s_keys=None,
            s_dates=None, s_coco=None, s_city=None, s_geo=None, s_geo_lat=None,
            s_geo_long=None, s_geo_rad_km=None, s_src=None, s_area=None,
            s_ven=None, s_eve=None, s_class=None, event_token_list=None,
            request_source_info=None, request_extra_info=None,
            request_video_iframe=None, request_cost_range=None,
            request_media=None, request_custom_fields=None,
            request_reviews=None, request_avail_details=None,
            s_top=None, s_user_rating=None, s_critic_rating=None,
            s_auto_range=None, page_length=None, page_number=None,
            s_cust_fltr=None, s_airport=None, mime_text_type=None,
            request_meta_components=None,
    ):
        if crypto_block is None:
            user_passwd = self.password
        else:
            user_passwd = None

        resp = self.make_core_request(
            'event_search',
            user_passwd=user_passwd, crypto_block=crypto_block,
            upfront_data_token=upfront_data_token, s_keys=s_keys,
            s_dates=s_dates, s_coco=s_coco, s_geo=s_geo, s_geo_lat=s_geo_lat,
            s_geo_long=s_geo_long, s_geo_rad_km=s_geo_rad_km, s_src=s_src,
            s_area=s_area, s_ven=s_ven, s_eve=s_eve, s_class=s_class,
            s_city=s_city, event_token_list=event_token_list,
            request_source_info=request_source_info,
            request_extra_info=request_extra_info,
            request_video_iframe=request_video_iframe,
            request_cost_range=request_cost_range,
            request_media=request_media,
            request_custom_fields=request_custom_fields,
            request_avail_details=request_avail_details,
            s_top=s_top, s_user_rating=s_user_rating,
            s_critic_rating=s_critic_rating,
            s_auto_range=s_auto_range, page_length=page_length,
            page_number=page_number,
            s_cust_fltr=s_cust_fltr,
            request_reviews=request_reviews,
            s_airport=s_airport,
            mime_text_type=mime_text_type,
            request_meta_components=request_meta_components,
        )

        return self.parse_response(parse.event_search_result, resp)

    def extra_info(
            self, crypto_block, event_token, upfront_data_token=None,
            source_info=None, request_media=None,
            mime_text_type=None, request_avail_details=None):
        resp = self.make_core_request(
            'extra_info',
            crypto_block=crypto_block, upfront_data_token=upfront_data_token,
            event_token=event_token, source_info=source_info,
            request_media=request_media, mime_text_type=mime_text_type,
            request_avail_details=request_avail_details,
        )

        return self.parse_response(parse.extra_info_result, resp)

    def date_time_options(
            self, crypto_block, event_token, upfront_data_token=None,
            earliest_date=None, latest_date=None, request_cost_range=None,
            page_length=None, page_number=None):
        resp = self.make_core_request(
            'date_time_options',
            crypto_block=crypto_block, event_token=event_token,
            upfront_data_token=upfront_data_token, earliest_date=earliest_date,
            latest_date=latest_date, request_cost_range=request_cost_range,
            page_length=page_length, page_number=page_number,
        )

        return self.parse_response(parse.date_time_options_result, resp)

    def month_options(
            self, crypto_block, event_token, upfront_data_token=None):
        resp = self.make_core_request(
            'month_options',
            crypto_block=crypto_block,
            event_token=event_token,
            upfront_data_token=upfront_data_token,
        )

        return self.parse_response(parse.month_options_result, resp)

    def availability_options(
            self, crypto_block, upfront_data_token=None, perf_token=None,
            departure_date=None, usage_date=None, self_print_mode=None,
            trolley_token=None, add_discounts=None, quantity_options_only=None,
            no_of_tickets=None, add_free_seat_blocks=None,
            add_user_commission=None):

        resp = self.make_core_request(
            'availability_options',
            crypto_block=crypto_block, upfront_data_token=upfront_data_token,
            perf_token=perf_token, departure_date=departure_date,
            usage_date=usage_date, self_print_mode=self_print_mode,
            trolley_token=trolley_token, add_discounts=add_discounts,
            quantity_options_only=quantity_options_only,
            no_of_tickets=no_of_tickets,
            add_free_seat_blocks=add_free_seat_blocks,
            add_user_commission=add_user_commission,
        )

        return self.parse_response(parse.availability_options_result, resp)

    def despatch_options(
            self, crypto_block, upfront_data_token=None, perf_token=None,
            departure_date=None, usage_date=None, self_print_mode=None,
            trolley_token=None):

        resp = self.make_core_request(
            'despatch_options',
            crypto_block=crypto_block, upfront_data_token=upfront_data_token,
            perf_token=perf_token, departure_date=departure_date,
            usage_date=usage_date, self_print_mode=self_print_mode,
            trolley_token=trolley_token,
        )

        return self.parse_response(parse.despatch_options_result, resp)

    def discount_options(
            self, crypto_block, band_token, no_of_tickets,
            upfront_data_token=None, despatch_token=None, trolley_token=None,
            seat_block_token=None, seat_block_offset=None,
            add_user_commission=None):
        resp = self.make_core_request(
            'discount_options',
            crypto_block=crypto_block,
            band_token=band_token, despatch_token=despatch_token,
            no_of_tickets=no_of_tickets, upfront_data_token=upfront_data_token,
            trolley_token=trolley_token, seat_block_token=seat_block_token,
            seat_block_offset=seat_block_offset,
            add_user_commission=add_user_commission,
        )

        return self.parse_response(parse.discount_options_result, resp)

    def create_order(
            self, crypto_block, upfront_data_token=None, discount_token=None,
            despatch_token=None):
        resp = self.make_core_request(
            'create_order',
            crypto_block=crypto_block, upfront_data_token=upfront_data_token,
            discount_token=discount_token, despatch_token=despatch_token,
        )

        return self.parse_response(parse.create_order_result, resp)

    def create_order_and_reserve(
            self, crypto_block, upfront_data_token=None, discount_token=None,
            despatch_token=None):
        resp = self.make_core_request(
            'create_order_and_reserve',
            crypto_block=crypto_block, upfront_data_token=upfront_data_token,
            discount_token=discount_token, despatch_token=despatch_token,
        )

        return self.parse_response(parse.create_order_and_reserve_result, resp)

    def trolley_add_order(
            self, crypto_block, order_token, upfront_data_token=None,
            trolley_token=None, describe_trolley=None):
        resp = self.make_core_request(
            'trolley_add_order',
            crypto_block=crypto_block, order_token=order_token,
            upfront_data_token=upfront_data_token, trolley_token=trolley_token,
            describe_trolley=describe_trolley,
        )

        return self.parse_response(parse.trolley_add_order_result, resp)

    def trolley_describe(
            self, crypto_block, trolley_token, upfront_data_token=None):
        resp = self.make_core_request(
            'trolley_describe',
            crypto_block=crypto_block, trolley_token=trolley_token,
            upfront_data_token=upfront_data_token,
        )

        return self.parse_response(parse.trolley_describe_result, resp)

    def trolley_remove(
            self, crypto_block, trolley_token, upfront_data_token=None,
            remove_item=None, describe_trolley=None):
        resp = self.make_core_request(
            'trolley_remove',
            crypto_block=crypto_block, trolley_token=trolley_token,
            upfront_data_token=upfront_data_token, remove_item=remove_item,
            describe_trolley=describe_trolley,
        )

        return self.parse_response(parse.trolley_remove_result, resp)

    def make_reservation(
            self, crypto_block, trolley_token, upfront_data_token=None,
            self_print_mode=None, describe_trolley=None):
        resp = self.make_core_request(
            'make_reservation',
            crypto_block=crypto_block, trolley_token=trolley_token,
            upfront_data_token=upfront_data_token,
            self_print_mode=self_print_mode,
            describe_trolley=describe_trolley,
        )

        return self.parse_response(parse.make_reservation_result, resp)

    def get_reservation_link(
            self, crypto_block, trolley_token, upfront_data_token=None):
        resp = self.make_core_request(
            'get_reservation_link',
            crypto_block=crypto_block, trolley_token=trolley_token,
            upfront_data_token=upfront_data_token,
        )

        return self.parse_response(parse.get_reservation_link_result, resp)

    def release_reservation(
            self, crypto_block, upfront_data_token=None):
        resp = self.make_core_request(
            'release_reservation',
            crypto_block=crypto_block, upfront_data_token=upfront_data_token,
        )

        return self.parse_response(parse.release_reservation_result, resp)

    def purchase_reservation_part_one(
            self, crypto_block, customer_data, return_token, return_domain,
            return_path, return_with_https, encryption_key, card_data=None,
            user_can_use_data=None, supplier_can_use_data=None,
            world_can_use_data=None, upfront_data_token=None):
        resp = self.make_core_request(
            'purchase_reservation_part_one',
            crypto_block=crypto_block, customer_data=customer_data,
            return_token=return_token, return_domain=return_domain,
            return_path=return_path, return_with_https=return_with_https,
            encryption_key=encryption_key, card_data=card_data,
            user_can_use_data=user_can_use_data,
            supplier_can_use_data=supplier_can_use_data,
            world_can_use_data=world_can_use_data,
            upfront_data_token=upfront_data_token,
        )

        return self.parse_response(
            parse.purchase_reservation_part_one_result, resp
        )

    def purchase_reservation_part_two(
            self, returning_token, new_return_token, new_return_path, http_referer,
            http_accept, http_user_agent, callback_data, encryption_key,
            crypto_block=None, send_confirmation_email=None, results_url=None,
            upfront_data_token=None):

        if crypto_block is None:
            user_passwd = self.password
        else:
            user_passwd = None

        resp = self.make_core_request(
            'purchase_reservation_part_two',
            user_passwd=user_passwd,
            crypto_block=crypto_block,
            upfront_data_token=upfront_data_token,
            returning_token=returning_token,
            new_return_token=new_return_token,
            new_return_path=new_return_path,
            http_referer=http_referer, http_accept=http_accept,
            http_user_agent=http_user_agent, callback_data=callback_data,
            encryption_key=encryption_key,
            send_confirmation_email=send_confirmation_email,
            results_url=results_url,
        )

        return self.parse_response(
            parse.purchase_reservation_part_two_result, resp
        )

    def purchase_reservation(
            self, crypto_block, customer_data, card_data=None,
            send_confirmation_email=None,
            upfront_data_token=None):

        resp = self.make_core_request(
            'purchase_reservation',
            crypto_block=crypto_block, customer_data=customer_data,
            card_data=card_data,
            send_confirmation_email=send_confirmation_email,
            upfront_data_token=upfront_data_token,
        )

        return self.parse_response(
            parse.purchase_reservation, resp
        )

    def transaction_info(
            self, transaction_id, describe_trolley=None, describe_customer=None,
            describe_external_sale_page=None, crypto_block=None,
            upfront_data_token=None):

        if crypto_block is None:
            user_passwd = self.password
        else:
            user_passwd = None

        resp = self.make_core_request(
            'transaction_info',
            user_passwd=user_passwd,
            transaction_id=transaction_id,
            describe_trolley=describe_trolley,
            describe_customer=describe_customer,
            describe_external_sale_page=describe_external_sale_page,
            crypto_block=crypto_block, upfront_data_token=upfront_data_token,
        )

        return self.parse_response(parse.transaction_info_result, resp)

    def save_external_sale_page(
            self, transaction_id, sale_page_type, sale_page_subtype, sale_page,
            crypto_block=None, upfront_data_token=None):

        if crypto_block is None:
            user_passwd = self.password
        else:
            user_passwd = None

        resp = self.make_core_request(
            'save_external_sale_page',
            user_passwd=user_passwd,
            crypto_block=crypto_block,
            upfront_data_token=upfront_data_token,
            transaction_id=transaction_id,
            sale_page_type=sale_page_type,
            sale_page_subtype=sale_page_subtype,
            sale_page=sale_page,
        )

        return self.parse_response(parse.save_external_sale_page_result, resp)
