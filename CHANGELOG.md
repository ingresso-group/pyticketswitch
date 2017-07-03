# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [2.0.6] - 2017-07-03
### Added
- Purchase Result information at the bundle level

## [2.0.5] - 2017-06-22
### Fixed
- Fixed a bug when custom tracking id would not overwrite global one.
### Added
- Tests/Documentation for custom Tracking id feature

## [2.0.4] - 2017-06-19
### Fixed
- Reservation object now handles unreserved orders correctly.
### Added
- Added ability to set tracking ID for pyticketswitch requests

## [2.0.3] - 2017-06-07
### Added
- Added `final_comment` to the SendMethod class. This was present in the XML
  but got lost when we switched to JSON.

## [2.0.2] - 2017-06-05
### Added
- A new client call to the `upsells.v1` endpoint
- A new client call to the `add_ons.v1` endpoint
- New behavioural and unit tests for this functionality
- Added `is_add_on` property to Event
- `get_events` now supports adding upsell and add-on information to Events

## [2.0.1] - 2017-06-01
### Fixed
- incorrect sub user parameter being passed to the API was sub_user should
  have been sub_id.

### Updated
- Some behavioural tests improved
- PyDoc links to API documentation
- Legacy API documentation

## [2.0.0] - 2017-05-05
### Added
- A new wrapper for the JSON API.
- Comprehensive unit and behavioural tests.
- Up-to-date docs.

### Removed
- The XML API has been deprecated in favour of the new JSON API. As such we
  have used this as opportunity to clean up the turgid shit show that was the
  previous api wrapper, and replace it with some thing alot cleaner. If you
  still want to use the XML API and wrapper then pin your repos at 1.13.1 as
  this will be last version of this library that will support it. The XML API
  is not likely to go away anytime soon and the wrapper should continue to 
  work.
- TL;DR everything was removed and rewritten.

## 1.12.0 - 2016-06-13
- python3 now supported, travis config updated to reflect this.

## 1.11.2 - 2016-06-10
- Fix special offer search ordering and add 'excluded_events_list' param to event_search

## 1.11.1 - 2016-06-17
- Use unicode literals everywhere

## 1.11.0 - 2016-05-12
- Removed internal api call, add custom start session method

## 1.10.1 - 2016-04-29
- Removed logging of exceptions on API errors

## 1.10.0 - 2016-04-27
- Added all __future__ imports to files as a step towards Python 3 compatibility.

## 1.9.1 - 2016-04-21
- Add meta_event (e.g. touring shows) support.

## 1.9.0 - 2016-04-20
- Mock API calls in tests using VCR.py.

## 1.8.7 - 2016-02-16
- Add properties to TicketType object.

## 1.8.4 - 2015-12-16
- Add project to Travis and add code coverage

## 1.8.3 - 2015-12-08
- Add 'has_no_perfs' flag to Event object.

## 1.8.2 - 2015-12-02
- Revert changes to raise BackendCallFailure until better solution.

## 1.8.1 - 2015-11-26
- Bugfix - passing in sub_id of None to start_session.

## 1.8.0 - 2015-11-20
- Switch to using Requests instead of urllib2.

## 1.7.4 - 2015-10-22
- Add properties to TicketType and Concession objects.

## 1.7.2 - 2015-10-15
- Add 'barcode' to Seat object.

## 1.7.1 - 2015-10-08
- Add new properties to AvailDetail class.

## 1.7.0 - 2015-08-25
- Add Commission object, used for representing user and gross commissions. Commissions now returned at availability and purchase time.

## 1.6.5 - 2015-08-19
- Fix bug with using alternate billing address

## 1.6.4 - 2015-08-10
- update license and setup files

## 1.6.3 - 2015-08-10
- Add 'separator' attribute to Seat object

## 1.6.2 - 2015-08-07
- Add 'purchase_reservation' call for purchases made on credit

## 1.6.1 - 2015-08-03
- Add additional order information attributes

## 1.6.0 - 2015-07-03
- Modify how seat blocks are passed into get_concessions()

## 1.5.3 - 2015-06-30
- Add page_length and page_number to datetime search

## 1.5.2 - 2015-06-22
- Change default start session URL to use HTTPS

## 1.5.1 - 2015-05-06
- Fix a potential caching issue when getting valid ticket quantities from an event

## 1.5.0 - 2015-06-05
- Add support for upfront data. This is required by the core for redeem users.

## 1.4.17 - 2015-04-01
- For special offer event searches add max_iterations argument to improve performance with the trade-off of not guaranteeing returning all results.

## 1.4.16 - 2015-03-26
- Add has_no_booking_fee property to AvailDetail.

## 1.4.15 - 2015-03-26
- Add avail_details_by_cheapest_ticket_type method to Event.

## 1.4.14 - 2015-03-16
- Prevent event avail details being cached.

## 1.4.13 - 2015-03-13
- Add AvailDetail object to event (represents detailed pricing information).

## 1.4.12 - 2015-03-11
- Couple of minor fixes, including one for handling no availability in reserve.

## 1.4.11 - 2015-02-24
- Minor restrict_group change.

## 1.4.10 - 2015-02-13
- Spelling mistake in API output fixed.

## 1.4.9 - 2015-01-29
- Set mime_text_type to 'html' for event extra_info call

## 1.4.8 - 2015-01-14
- Fix bug when no 'event_quantity_options' in extra_info

## 1.4.7 - 2015-01-08
- Add no_singles cost range object to CostRangeMixin and add valid_ticket_quantities method to Event

## 1.4.6 - 2014-12-12
- Minor logging change.

## 1.4.5 - 2014-12-11
- Add code attributes to Concession and Despatch methods, add perf_type_code to Performance and add price_band_code to TicketType.

## 1.4.4 - 2014-12-05
- Add the ability to include additional elements in the XML passed to the API.

## 1.4.3 - 2014-12-04
- Order object changes relating to requested seats, add restricted view attributes to ticket type, changes to purchase exceptions.

## 1.4.2 - 2014-12-02
- Change how special offers are handled, add functionality to check if an offer is a no booking fee offer.

## 1.4.1 - 2014-11-19
- Add support for retrieving event structured content.

## 1.4.0 - 2014-11-18
- Add Currency object and remove core_currency references, add support for retrieving user commission information and structured event information, include price band descriptions in ticket type description.

## 1.3.0 - 2014-10-29
- Change 'number_available' attribute to be integer, add total_seats and contiguous_seats attributes to the TicketType and Concession objects.

## 1.2.3 - 2014-10-28
- Fix bug with logging and minor bug with the Performance object.

## 1.2.2 - 2014-10-27
- Fix bug with Seats that have no column/row id.

## 1.2.1 - 2014-10-24
- Fix bug with Seat object not parsing for some unreserved seats/

## 1.2.0 - 2014-10-23
- Add support for selecting specific seats, bug fix in creating reservation.

## 1.1.3 - 2014-10-17
- Add discount attributes to core price_band object.

## 1.1.2 - 2014-10-13
- Add remote_site attribute in Reservation.

## 1.1.1 - 2014-10-13
- Added languages attribute to Customer.

## 1.1.0 - 2014-10-09
- Support for actual seats, retrieving quantity options without availability, new event images.

## 1.0.3 - 2014-10-03
- Fix bug in availability objects.

## 1.0.2 - 2014-09-17
- Change to get_concessions docs.

## 1.0.1 - 2014-09-10
- Fix bug with confirmation emails.

## 1.0.0 - 2014-09-08
- Initial release.

[Unreleased]: https://github.com/ingresso-group/pyticketswitch/compare/2.0.1...HEAD
[2.0.5]: https://github.com/ingresso-group/pyticketswitch/compare/2.0.4...2.0.5
[2.0.4]: https://github.com/ingresso-group/pyticketswitch/compare/2.0.3...2.0.4
[2.0.1]: https://github.com/ingresso-group/pyticketswitch/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/ingresso-group/pyticketswitch/compare/1.13.1...2.0.0

