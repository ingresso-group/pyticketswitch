# EXAMPLE USAGE

from pyticketswitch import (
    Core, Trolley, Customer, Address, Card
)

session = {}

settings = {
    'username': 'testuser',
    'password': 'testpassword',
    'url': 'https://testuser.tsd-aff.com/cgi-bin/xml_core.exe',
    'session': session
}

core = Core(**settings)

# Perform an event search, returning a list of events
events = core.search_events(keyword='nutcracker')

# select an Event object from the list
for e in events:
    print e.event_id, e.description
    if e.event_id == '6IF':
        event = e

# Or event = Event(event_id=<event_id>, **settings)

# get the list of performances for this event
performances = event.performances

# select a performance
for p in performances:
    print p.date_desc, p.time_desc
    if (
        p.date_desc == 'Mon, 6th October 2014'
        and p.time_desc == '7.30 PM'
    ):
        performance = p

# Or performance = Performance(perf_id=<perf_id>, **settings)

# get the list of TicketType objects
ticket_types = performance.ticket_types

# select a TicketType
for tt in ticket_types:
    print tt.description, tt.price_combined_float, tt.number_available
    if (
        tt.description == 'Upper circle'
        and tt.price_combined_float == 34.0
    ):
        ticket_type = tt

# get the list of lists of concessions (one list of concessions
# per ticket requested)
concession_sets = ticket_type.get_concessions(no_of_tickets=2)

# for each ticket, select a concession
selected_concessions = []
for concession_list in concession_sets:
    for c in concession_list:
        print c.description, c.ticket_price_float
        if c.description == 'Adult standard':
            selected_concessions.append(c)

# get list of despatch methods available on this performance
despatch_methods = performance.despatch_methods

for dm in despatch_methods:
    print dm.description, dm.cost_float

# select a despatch method
despatch_method = despatch_methods[0]

# create the order by passing a list of concessions and the
# selected despatch_method
order = core.create_order(
    concessions=selected_concessions,
    despatch_method=despatch_method
)

# Create a trolley
trolley = Trolley(**settings)

# Add the order to the trolley
trolley.add_order(order)

# Multiple orders can be added to the trolley
# Once an order has been added, Trolleys are made up of 'bundles'
# These are groups of orders (per supplier system)
# So cost information can be retrieved at this level (e.g.
# trolley.bundles, then bundle.total_cost)

# When ready to purchase, the trolley can be reserved
reservation = trolley.get_reservation()

"""
Reservation is a subclass of Trolley, so shares some of the same
functionality

Usually reservations are valid for 10 minutes, so a purchase
must be completed in this time

The purchase process is split into 2 methods, purchase_part_one
and purchase_part_two. The first returns an address that the user's
browser must be redirected to, then on return, purchase_part_two
must be called to complete the purchase.

To get a better idea of how this process works, there is
documentation available here:
    http://www.ingresso.co.uk/apidocs/old-doc/api-doc2.html

Because of the need to redirect the user's browser, it is difficult
to demonstrate here, but some example calls are below.
"""

# Create an address object for the customer's address
# The country code is a 2 digit ISO 3166 country code
customer_address = Address(
    address_line_one='1 Test Lane',
    address_line_two=None,
    town='Test Town',
    county='County',
    postcode='AB12 3CD',
    country_code='GB'
)

# Create a customer object
customer = Customer(
    title='Mr',
    first_name='Test',
    last_name='User',
    email_address='test@test.com',
    home_phone='01234567890',
    work_phone='01234567890',
    address=customer_address,
    user_can_use_data=True,
    supplier_can_use_data=False,
    world_can_use_data=False
)

import datetime

# create a card object
card = Card(
    card_number='1234567891011121',
    start_date=datetime.date(2014, 1, 1),
    expiry_date=datetime.date(2016, 1, 1),
    cv_two='123',
    issue_number='1',
    billing_address=None
)

# The response dictionary will contain an item called
# 'redirect_html_page_data' which consists of a string of
# HTML to pass to the user's browser. It contains a javascript
# redirect to an external page.
response_one_dictionary = reservation.purchase_part_one(
    return_token='<unique token to identify request>',
    return_domain='<return domain>',
    return_path='<return path>',
    return_with_https=True or False,
    encryption_key='<see documentation>',
    customer=customer,
    card=card,
)

# The response dictionary here will contain an item called
# 'self_print_html_pages' if there were any self print orders.
# Other than that the response will contain 'trolley' and
# 'customer' elements.
response_two_dictionary = reservation.purchase_part_two(
    returning_token='<token returned by part_one_redirect>',
    new_return_token='<unique token to identify request>',
    new_return_path='<return path>',
    http_referer='<HTTP Referer header>',
    http_accept='<HTTP Accept header>',
    http_user_agent='<HTTP User-Agent header>',
    callback_data='<All POST and GET variables, plus any variables from the query string>',
    encryption_key='<see documentation>',
    send_confirmation_email=True or False,
)
