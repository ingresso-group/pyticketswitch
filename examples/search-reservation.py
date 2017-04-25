import random
from pyticketswitch import Client

client = Client('demo', 'demopass')


print("")
print("events.v1")
events = client.list_events()
for event in events:
    print(event.id, event.description)


print("")
print("events_by_id.v1:")
events = client.get_events(['6IF', '6IE'])

for event_id, event in events.items():
    print(event_id, event.description)

event = events['6IF']

print("")
print("performances.v1:")
performances = client.list_performances(event.id)
for performance in performances:
    print(performance.id, performance.date_time.isoformat())


print("")
print("performances_by_id.v1:")
performances = client.get_performances([
    performance.id
    for performance in random.sample(performances, 2)
])

for performance_id, performance in performances.items():
    print(performance_id, performance.date_time.isoformat())


print("")
print("availablity.v1:")
availability, meta = client.get_availability(performance.id)
print("contiguous seat selection only:", meta.contiguous_seat_selection_only)
print("currency:", meta.currency.code)
print("valid quantities: {}".format(','.join([str(x) for x in meta.valid_quantities])))

for ticket_type in availability:
    print(ticket_type.code)
    for price_band in ticket_type.price_bands:
        disc = price_band.default_discount
        print("   ", price_band.code, disc.code, disc.seatprice, disc.surcharge)
        print("allows_leaving_single_seats: '{}'".format(
            price_band.allows_leaving_single_seats))


print("")
print("trolley.v1:")
ticket_type = random.choice(availability)
price_band = random.choice(ticket_type.price_bands)
trolley = client.get_trolley(
    performance_id=performance.id,
    ticket_type_code=ticket_type.code,
    price_band_code=price_band.code,
    number_of_seats=2,
)

print("inital token:", trolley.token)
print("total:", trolley.bundles[0].total)

trolley = client.get_trolley(
    token=trolley.token,
    performance_id=performance.id,
    ticket_type_code=ticket_type.code,
    price_band_code=price_band.code,
    number_of_seats=4,
)

print("new token:", trolley.token)
print("total:", trolley.bundles[0].total)

print("")
print("reservation.v1:")
reservation = client.make_reservation(token=trolley.token)
print(reservation.trolley.random_index)
