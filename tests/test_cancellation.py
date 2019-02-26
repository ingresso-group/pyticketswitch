import pytest

from pyticketswitch.cancellation import CancellationResult


successful_cancellation_data = {
    "trolley_contents": {
        "trolley_bundle_count": 1,
        "trolley_order_count": 1,
        "bundle": [
            {
                "bundle_total_seatprice": 32,
                "bundle_total_send_cost": 1.5,
                "order": [
                    {
                        "price_band_code": "A/pool",
                        "internal_reserve_sub_ref2": "NUT SUB 2",
                        "backend_cancellation_reference": "ATTEMPT-482281",
                        "total_sale_surcharge": 5,
                        "item_number": 1,
                        "performance": {
                            "running_time": 120,
                            "has_pool_seats": True,
                            "event_id": "6IF",
                            "time_desc": "7.30 PM",
                            "is_limited": False,
                            "perf_id": "6IF-D9P",
                            "is_ghost": False,
                            "iso8601_date_and_time": "2019-04-26T19:30:00+01:00",
                            "date_desc": "Fri, 26th April 2019",
                        },
                        "backend_purchase_reference": "PURCHASE-286D",
                        "user_commission": {
                            "amount_including_vat": 11.4,
                            "commission_currency_code": "gbp",
                            "amount_excluding_vat": 9.5,
                        },
                        "send_method": {
                            "send_cost": 1.5,
                            "send_desc": "Collect from venue",
                            "send_final_comment": "Instructions for collecting tickets at the venue box office:\n- Tickets must be collected by the cardholder with valid photo identification and the payment card.\n- The cardholderâs signature will be required on receipt of these tickets.\n- Tickets are only available for collection on the day of the performance.\n- Guests are advised to arrive at least 30 minutes before the performance time.\n- If the cardholder is unable to collect these tickets please contact Guest Services on 0800 640 8101.\n\nCan we help?\nIf you require further information please contact our Guest Services team:\nLive chat or call 0800 640 8101 (Monday â Sunday, 9am â 9pm GMT/BST)",
                            "send_type": "collect",
                            "send_code": "COBO",
                            "send_final_type": "collect",
                        },
                        "ticket_type_desc": "Stalls",
                        "gross_commission": {
                            "amount_including_vat": 11.4,
                            "amount_excluding_vat": 9.5,
                            "commission_currency_code": "gbp",
                        },
                        "cancellation_status": "cancelled",
                        "ticket_orders": {
                            "ticket_order": [
                                {
                                    "total_sale_seatprice": 21,
                                    "sale_surcharge": 3,
                                    "total_sale_combined": 24,
                                    "sale_seatprice": 21,
                                    "seats": [
                                        {
                                            "full_id": "YG167",
                                            "is_restricted_view": False,
                                            "col_id": "167",
                                            "row_id": "YG",
                                        }
                                    ],
                                    "discount_code": "ADULT",
                                    "discount_desc": "Adult standard",
                                    "sale_combined": 24,
                                    "total_sale_surcharge": 3,
                                    "no_of_seats": 1,
                                },
                                {
                                    "total_sale_surcharge": 2,
                                    "sale_combined": 13,
                                    "discount_desc": "Adult 18+ including behind the scenes tour",
                                    "discount_code": "CHILD",
                                    "no_of_seats": 1,
                                    "sale_surcharge": 2,
                                    "total_sale_seatprice": 11,
                                    "seats": [
                                        {
                                            "row_id": "YG",
                                            "col_id": "168",
                                            "is_restricted_view": False,
                                            "full_id": "YG168",
                                        }
                                    ],
                                    "sale_seatprice": 11,
                                    "total_sale_combined": 13,
                                },
                            ]
                        },
                        "cancellation_comment": "",
                        "total_sale_combined": 37,
                        "total_no_of_seats": 2,
                        "price_band_desc": "Top price (band A)",
                        "seat_request_status": "not_requested",
                        "ticket_type_code": "STALLS",
                        "total_sale_seatprice": 32,
                        "event": {
                            "has_no_perfs": False,
                            "min_running_time": 120,
                            "need_departure_date": False,
                            "need_duration": False,
                            "city_code": "london-uk",
                            "show_perf_time": True,
                            "is_seated": True,
                            "event_uri_desc": "Matthew-Bourne%27s-Nutcracker%21",
                            "source_code": "ext_test0",
                            "source_desc": "Test SystemZero for on-credit backend group",
                            "event_desc": "Matthew Bourne's Nutcracker!",
                            "event_type": "simple_ticket",
                            "event_status": "live",
                            "event_upsell_list": {"event_id": ["6IE", "6KU"]},
                            "venue_uri_desc": "Sadler%27s-Wells",
                            "critic_review_percent": 80,
                            "country_desc": "United Kingdom",
                            "venue_desc": "Sadler's Wells",
                            "max_running_time": 120,
                            "geo_data": {"latitude": 51.5, "longitude": -0.15},
                            "event_id": "6IF",
                            "need_performance": True,
                            "postcode": "EC1R 4TN",
                            "city_desc": "London",
                            "is_add_on": False,
                            "country_code": "uk",
                            "classes": {"theatre": "Theatre"},
                            "is_auto_quantity_add_on": False,
                            "custom_filter": [],
                        },
                        "internal_reserve_sub_ref": "NUT SUB 1",
                        "requested_seat_ids": [],
                        "internal_purchase_sub_ref": "SUBREF-1:NUT SUB 2:NUT SUB 1",
                    }
                ],
                "purchase_result": {
                    "can_cancel_individual_orders": False,
                    "success": True,
                    "backend_purchase_reference": "PURCHASE-286D",
                    "is_semi_credit": False,
                },
                "bundle_total_surcharge": 5,
                "bundle_order_count": 1,
                "bundle_source_code": "ext_test0",
                "bundle_total_cost": 38.5,
                "bundle_source_desc": "Test SystemZero for on-credit backend group",
                "currency_code": "gbp",
            }
        ],
        "transaction_uuid": "284d9c3a-d698-11e6-be8c-002590326962",
        "purchase_result": {"success": True, "is_partial": False},
        "transaction_id": "U000-0000-2M96-DEVX",
    },
    "currency_details": {
        "gbp": {
            "currency_pre_symbol": "Â£",
            "currency_post_symbol": "",
            "currency_factor": 100,
            "currency_code": "gbp",
            "currency_number": 826,
            "currency_places": 2,
        }
    },
    "cancelled_item_numbers": [1],
}

partial_cancellation_data = {
   "trolley_contents" : {
      "trolley_bundle_count" : 1,
      "trolley_order_count" : 2,
      "bundle" : [
         {
            "bundle_total_seatprice" : 64,
            "bundle_total_send_cost" : 3,
            "order" : [
               {
                  "price_band_code" : "A/pool",
                  "internal_reserve_sub_ref2" : "NUT SUB 2",
                  "backend_cancellation_reference" : "ATTEMPT-482281",
                  "total_sale_surcharge" : 5,
                  "item_number" : 1,
                  "performance" : {
                     "running_time" : 120,
                     "has_pool_seats" : True,
                     "event_id" : "6IF",
                     "time_desc" : "7.30 PM",
                     "is_limited" : False,
                     "perf_id" : "6IF-D9P",
                     "is_ghost" : False,
                     "iso8601_date_and_time" : "2019-04-26T19:30:00+01:00",
                     "date_desc" : "Fri, 26th April 2019"
                  },
                  "backend_purchase_reference" : "PURCHASE-286D",
                  "user_commission" : {
                     "amount_including_vat" : 11.4,
                     "commission_currency_code" : "gbp",
                     "amount_excluding_vat" : 9.5
                  },
                  "send_method" : {
                     "send_cost" : 1.5,
                     "send_desc" : "Collect from venue",
                     "send_final_comment" : "Instructions for collecting tickets at the venue box office:\n- Tickets must be collected by the cardholder with valid photo identification and the payment card.\n- The cardholderâs signature will be required on receipt of these tickets.\n- Tickets are only available for collection on the day of the performance.\n- Guests are advised to arrive at least 30 minutes before the performance time.\n- If the cardholder is unable to collect these tickets please contact Guest Services on 0800 640 8101.\n\nCan we help?\nIf you require further information please contact our Guest Services team:\nLive chat or call 0800 640 8101 (Monday â Sunday, 9am â 9pm GMT/BST)",
                     "send_type" : "collect",
                     "send_code" : "COBO",
                     "send_final_type" : "collect"
                  },
                  "ticket_type_desc" : "Stalls",
                  "gross_commission" : {
                     "amount_including_vat" : 11.4,
                     "amount_excluding_vat" : 9.5,
                     "commission_currency_code" : "gbp"
                  },
                  "cancellation_status" : "cancelled",
                  "ticket_orders" : {
                     "ticket_order" : [
                        {
                           "total_sale_seatprice" : 21,
                           "sale_surcharge" : 3,
                           "total_sale_combined" : 24,
                           "sale_seatprice" : 21,
                           "seats" : [
                              {
                                 "full_id" : "YG167",
                                 "is_restricted_view" : False,
                                 "col_id" : "167",
                                 "row_id" : "YG"
                              }
                           ],
                           "discount_code" : "ADULT",
                           "discount_desc" : "Adult standard",
                           "sale_combined" : 24,
                           "total_sale_surcharge" : 3,
                           "no_of_seats" : 1
                        },
                        {
                           "total_sale_surcharge" : 2,
                           "sale_combined" : 13,
                           "discount_desc" : "Adult 18+ including behind the scenes tour",
                           "discount_code" : "CHILD",
                           "no_of_seats" : 1,
                           "sale_surcharge" : 2,
                           "total_sale_seatprice" : 11,
                           "seats" : [
                              {
                                 "row_id" : "YG",
                                 "col_id" : "168",
                                 "is_restricted_view" : False,
                                 "full_id" : "YG168"
                              }
                           ],
                           "sale_seatprice" : 11,
                           "total_sale_combined" : 13
                        }
                     ]
                  },
                  "cancellation_comment" : "",
                  "total_sale_combined" : 37,
                  "total_no_of_seats" : 2,
                  "price_band_desc" : "Top price (band A)",
                  "seat_request_status" : "not_requested",
                  "ticket_type_code" : "STALLS",
                  "total_sale_seatprice" : 32,
                  "event" : {
                     "has_no_perfs" : False,
                     "min_running_time" : 120,
                     "need_departure_date" : False,
                     "need_duration" : False,
                     "city_code" : "london-uk",
                     "show_perf_time" : True,
                     "is_seated" : True,
                     "event_uri_desc" : "Matthew-Bourne%27s-Nutcracker%21",
                     "source_code" : "ext_test0",
                     "source_desc" : "Test SystemZero for on-credit backend group",
                     "event_desc" : "Matthew Bourne's Nutcracker!",
                     "event_type" : "simple_ticket",
                     "event_status" : "live",
                     "event_upsell_list" : {
                        "event_id" : [
                           "6IE",
                           "6KU"
                        ]
                     },
                     "venue_uri_desc" : "Sadler%27s-Wells",
                     "critic_review_percent" : 80,
                     "country_desc" : "United Kingdom",
                     "venue_desc" : "Sadler's Wells",
                     "max_running_time" : 120,
                     "geo_data" : {
                        "latitude" : 51.5,
                        "longitude" : -0.15
                     },
                     "event_id" : "6IF",
                     "need_performance" : True,
                     "postcode" : "EC1R 4TN",
                     "city_desc" : "London",
                     "is_add_on" : False,
                     "country_code" : "uk",
                     "classes" : {
                        "theatre" : "Theatre"
                     },
                     "is_auto_quantity_add_on" : False,
                     "custom_filter" : []
                  },
                  "internal_reserve_sub_ref" : "NUT SUB 1",
                  "requested_seat_ids" : [],
                  "internal_purchase_sub_ref" : "SUBREF-1:NUT SUB 2:NUT SUB 1"
               },
               {
                  "price_band_code" : "A/pool",
                  "internal_reserve_sub_ref2" : "CAT SUB 2",
                  "backend_cancellation_reference" : "ATTEMPT-482282",
                  "total_sale_surcharge" : 5,
                  "item_number" : 1,
                  "performance" : {
                     "running_time" : 120,
                     "has_pool_seats" : True,
                     "event_id" : "7AB",
                     "time_desc" : "3.30 PM",
                     "is_limited" : False,
                     "perf_id" : "7AB-7",
                     "is_ghost" : False,
                     "iso8601_date_and_time" : "2020-01-01T15:30:00+00:00",
                     "date_desc" : "Fri, 1st Jan 2020"
                  },
                  "backend_purchase_reference" : "PURCHASE-286D7",
                  "user_commission" : {
                     "amount_including_vat" : 11.4,
                     "commission_currency_code" : "gbp",
                     "amount_excluding_vat" : 9.5
                  },
                  "send_method" : {
                     "send_cost" : 1.5,
                     "send_desc" : "Collect from venue",
                     "send_final_comment" : "Instructions for collecting tickets at the venue box office:\n- Tickets must be collected by the cardholder with valid photo identification and the payment card.\n- The cardholderâs signature will be required on receipt of these tickets.\n- Tickets are only available for collection on the day of the performance.\n- Guests are advised to arrive at least 30 minutes before the performance time.\n- If the cardholder is unable to collect these tickets please contact Guest Services on 0800 640 8101.\n\nCan we help?\nIf you require further information please contact our Guest Services team:\nLive chat or call 0800 640 8101 (Monday â Sunday, 9am â 9pm GMT/BST)",
                     "send_type" : "collect",
                     "send_code" : "COBO",
                     "send_final_type" : "collect"
                  },
                  "ticket_type_desc" : "Stalls",
                  "gross_commission" : {
                     "amount_including_vat" : 11.4,
                     "amount_excluding_vat" : 9.5,
                     "commission_currency_code" : "gbp"
                  },
                  "cancellation_status" : "not_permitted",
                  "ticket_orders" : {
                     "ticket_order" : [
                        {
                           "total_sale_seatprice" : 21,
                           "sale_surcharge" : 3,
                           "total_sale_combined" : 24,
                           "sale_seatprice" : 21,
                           "seats" : [
                              {
                                 "full_id" : "E4",
                                 "is_restricted_view" : False,
                                 "col_id" : "4",
                                 "row_id" : "E"
                              }
                           ],
                           "discount_code" : "ADULT",
                           "discount_desc" : "Adult standard",
                           "sale_combined" : 24,
                           "total_sale_surcharge" : 3,
                           "no_of_seats" : 1
                        },
                        {
                           "total_sale_surcharge" : 2,
                           "sale_combined" : 13,
                           "discount_desc" : "Adult 18+ including behind the scenes tour",
                           "discount_code" : "CHILD",
                           "no_of_seats" : 1,
                           "sale_surcharge" : 2,
                           "total_sale_seatprice" : 11,
                           "seats" : [
                              {
                                 "row_id" : "E",
                                 "col_id" : "5",
                                 "is_restricted_view" : False,
                                 "full_id" : "E5"
                              }
                           ],
                           "sale_seatprice" : 11,
                           "total_sale_combined" : 13
                        }
                     ]
                  },
                  "cancellation_comment" : "",
                  "total_sale_combined" : 37,
                  "total_no_of_seats" : 2,
                  "price_band_desc" : "Top price (band A)",
                  "seat_request_status" : "not_requested",
                  "ticket_type_code" : "STALLS",
                  "total_sale_seatprice" : 32,
                  "event" : {
                     "has_no_perfs" : False,
                     "min_running_time" : 120,
                     "need_departure_date" : False,
                     "need_duration" : False,
                     "city_code" : "london-uk",
                     "show_perf_time" : True,
                     "is_seated" : True,
                     "event_uri_desc" : "The-Unremarkable-Incident-of-the-Cat-at-Lunchtime",
                     "source_code" : "ext_test0",
                     "source_desc" : "Test SystemZero for on-credit backend group",
                     "event_desc" : "The Unremarkable Incident of the Cat at Lunchtime",
                     "event_type" : "simple_ticket",
                     "event_status" : "live",
                     "event_upsell_list" : {
                        "event_id" : [
                           "6IE",
                           "6KU"
                        ]
                     },
                     "venue_uri_desc" : "Sadler%27s-Wells",
                     "critic_review_percent" : 80,
                     "country_desc" : "United Kingdom",
                     "venue_desc" : "Lyric Apollo",
                     "max_running_time" : 120,
                     "geo_data" : {
                        "latitude" : 51.5,
                        "longitude" : -0.15
                     },
                     "event_id" : "7AB",
                     "need_performance" : True,
                     "postcode" : "EC1R 4TN",
                     "city_desc" : "London",
                     "is_add_on" : False,
                     "country_code" : "uk",
                     "classes" : {
                        "theatre" : "Theatre"
                     },
                     "is_auto_quantity_add_on" : False,
                     "custom_filter" : []
                  },
                  "internal_reserve_sub_ref" : "CAT SUB 1",
                  "requested_seat_ids" : [],
                  "internal_purchase_sub_ref" : "SUBREF-1:CAT SUB 2:CAT SUB 1"
               }
            ],
            "purchase_result" : {
               "can_cancel_individual_orders" : False,
               "success" : True,
               "backend_purchase_reference" : "PURCHASE-286D",
               "is_semi_credit" : False
            },
            "bundle_total_surcharge" : 10,
            "bundle_order_count" : 2,
            "bundle_source_code" : "ext_test0",
            "bundle_total_cost" : 77,
            "bundle_source_desc" : "Test SystemZero for on-credit backend group",
            "currency_code" : "gbp"
         }
      ],
      "transaction_uuid" : "4df498e9-2daa-4393-a6bb-cc3dfefa7cc1",
      "purchase_result" : {
         "success" : True,
         "is_partial" : False
      },
      "transaction_id" : "U000-0000-2M96-DEVX"
   },
   "currency_details" : {
      "gbp" : {
         "currency_pre_symbol" : "£",
         "currency_post_symbol" : "",
         "currency_factor" : 100,
         "currency_code" : "gbp",
         "currency_number" : 826,
         "currency_places" : 2
      }
   },
   "cancelled_item_numbers" : [
      1
   ]
}


must_also_cancel_data = {
    "must_also_cancel": [
        {
            "cancellation_comment": "",
            "send_method": {
                "send_cost_in_desired": 8.76,
                "send_type": "post",
                "send_final_type": "post",
                "send_desc": "Post worldwide",
                "send_cost": 10,
                "send_code": "POST",
            },
            "ticket_orders": {
                "ticket_order": [
                    {
                        "seats": [
                            {
                                "is_restricted_view": False,
                                "row_id": "YC",
                                "full_id": "YC472",
                                "col_id": "472",
                            },
                            {
                                "full_id": "YC473",
                                "col_id": "473",
                                "row_id": "YC",
                                "is_restricted_view": False,
                            },
                            {
                                "col_id": "474",
                                "full_id": "YC474",
                                "row_id": "YC",
                                "is_restricted_view": False,
                            },
                        ],
                        "sale_combined_in_desired": 135.75,
                        "sale_surcharge_in_desired": 13.14,
                        "sale_seatprice": 140,
                        "total_sale_surcharge": 45,
                        "total_sale_combined": 465,
                        "discount_desc": "",
                        "total_sale_combined_in_desired": 407.24,
                        "sale_surcharge": 15,
                        "total_sale_surcharge_in_desired": 39.41,
                        "no_of_seats": 3,
                        "total_sale_seatprice": 420,
                        "sale_combined": 155,
                        "sale_seatprice_in_desired": 122.61,
                        "total_sale_seatprice_in_desired": 367.83,
                        "discount_code": "",
                    }
                ]
            },
            "total_sale_combined_in_desired": 407.24,
            "total_sale_seatprice": 420,
            "seat_request_status": "not_requested",
            "backend_cancellation_reference": "",
            "requested_seat_ids": [],
            "internal_purchase_sub_ref": "",
            "ticket_type_desc": "Menu French Cancan",
            "internal_reserve_sub_ref": "",
            "price_band_code": "A/pool",
            "user_commission": {
                "commission_currency_code": "eur",
                "amount_including_vat": 0,
                "amount_excluding_vat": 0,
            },
            "total_sale_combined": 465,
            "backend_purchase_reference": "PURCHASE-3AFD",
            "event": {
                "custom_filter": [],
                "min_running_time": 120,
                "geo_data": {"latitude": 0, "longitude": 0},
                "postcode": "75018",
                "event_id": "BPT",
                "venue_uri_desc": "Bal-du-Moulin-Rouge",
                "has_no_perfs": False,
                "need_performance": True,
                "source_code": "ext_test1",
                "event_uri_desc": "Moulin-Rouge-%28Dinner-Show%29",
                "event_type": "simple_ticket",
                "is_auto_quantity_add_on": False,
                "country_code": "fr",
                "venue_desc": "Bal du Moulin Rouge",
                "show_perf_time": True,
                "classes": {"attract": "Attractions", "theatre": "Theatre"},
                "source_desc": "Test System One",
                "max_running_time": 120,
                "event_status": "live",
                "need_departure_date": False,
                "need_duration": False,
                "event_desc": "Moulin Rouge (Dinner Show)",
                "country_desc": "France",
                "is_seated": True,
                "is_add_on": False,
            },
            "gross_commission": {
                "amount_including_vat": 60,
                "amount_excluding_vat": 50,
                "commission_currency_code": "eur",
            },
            "total_no_of_seats": 3,
            "ticket_type_code": "CANCAN",
            "performance": {
                "is_limited": False,
                "running_time": 120,
                "iso8601_date_and_time": "2019-04-01T19:00:00+02:00",
                "event_id": "BPT",
                "perf_id": "BPT-E6P",
                "date_desc": "Mon, 1st April 2019",
                "has_pool_seats": True,
                "is_ghost": False,
                "time_desc": "7.00 PM",
            },
            "total_sale_surcharge_in_desired": 39.41,
            "internal_reserve_sub_ref2": "",
            "cancellation_status": "possible",
            "total_sale_seatprice_in_desired": 367.83,
            "item_number": 2,
            "total_sale_surcharge": 45,
        }
    ],
    "currency_details": {
        "eur": {
            "currency_pre_symbol": "â¬",
            "currency_post_symbol": "",
            "currency_number": 978,
            "currency_code": "eur",
            "currency_places": 2,
            "currency_factor": 100,
        }
    },
}


class TestCancellationResult:
    def test_from_api_data_successful_cancellation(self):
        cancellation_result = CancellationResult.from_api_data(successful_cancellation_data)

        assert cancellation_result.cancelled_item_numbers == [1]
        assert len(cancellation_result.trolley.bundles) == 1
        assert len(cancellation_result.trolley.bundles[0].orders) == 1
        assert cancellation_result.must_also_cancel is None

    def test_from_api_data_must_also_cancel(self):
        cancellation_result = CancellationResult.from_api_data(must_also_cancel_data)

        assert len(cancellation_result.cancelled_item_numbers) == 0
        assert len(cancellation_result.trolley.bundles) == 0
        assert len(cancellation_result.must_also_cancel) == 1
        assert cancellation_result.must_also_cancel[0].item == 2

    @pytest.mark.parametrize(
        "data,expected_result",
        [
            (successful_cancellation_data, True),
            (must_also_cancel_data, False),
            (partial_cancellation_data, False)
        ],
    )
    def test_is_fully_cancelled(self, data, expected_result):
        cancellation_result = CancellationResult.from_api_data(data)

        assert cancellation_result.is_fully_cancelled() == expected_result



