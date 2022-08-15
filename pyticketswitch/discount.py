from pyticketswitch.mixins import JSONMixin, SeatPricingMixin
from pyticketswitch.commission import Commission


class Discount(SeatPricingMixin, JSONMixin, object):
    """Represents a set of prices for a price band.

    Attributes:
        code (str): the identifier for the discount.
        description (str): a human readable description for the discount.
        price_band_code (str): identifier for the related price band.
        is_offer (bool): indicates that the discount is an offer.
        availability (int): the number tickets available with this discount.
        percentage_saving (float): the amount saved compared to when this
            discount is not on offer, as a percentage or the non offer price.
        absolute_saving (float): the amount saved compared to when this
            discount is not on offer.
        gross_commission (:class: `Commission <pyticketswitch.commission.Commission>`):
            predicted commission to be shared between ingresso and the partner.
        user_commission (:class:`Commission <pyticketswitch.commission.Commission>`):
            predicted commission for the partner.
        disallowed_seat_nos (list): a list of seat numbers, that this discount
            code cannot be specified for.
        semantic_type: a mapping of the code to a meaning e.g. standard (adult) or child
        minimum_eligible_age: the youngest one can be to qualify for this ticket
        maximum_eligible_age: the oldest one can be to qualify for this ticket
    """

    def __init__(
        self,
        code,
        description=None,
        price_band_code=None,
        availability=None,
        is_offer=False,
        percentage_saving=0,
        absolute_saving=0,
        gross_commission=None,
        user_commission=None,
        disallowed_seat_nos=None,
        tax_component=None,
        semantic_type=None,
        minimum_eligible_age=None,
        maximum_eligible_age=None,
        *args,
        **kwargs
    ):
        super(Discount, self).__init__(*args, **kwargs)
        self.code = code
        self.description = description
        self.price_band_code = price_band_code
        self.is_offer = is_offer
        self.availability = availability
        self.percentage_saving = percentage_saving
        self.absolute_saving = absolute_saving
        self.gross_commission = gross_commission
        self.user_commission = user_commission
        self.disallowed_seat_nos = disallowed_seat_nos
        self.tax_component = tax_component
        self.semantic_type = semantic_type
        self.minimum_eligible_age = semantic_type
        self.maximum_eligible_age = semantic_type

    @classmethod
    def from_api_data(cls, data):
        """Creates a new Discount object from API data from ticketswitch.

        Args:
            data (dict): the part of the response from a ticketswitch API call
                that concerns a discount.

        Returns:
            :class:`Discount <pyticketswitch.discount.Discount>`: a new
            :class:`Discount <pyticketswitch.discount.Discount>` object
            populated with the data from the api.

        """
        gross_commission = data.get('predicted_gross_commission')
        if gross_commission:
            gross_commission = Commission.from_api_data(gross_commission)

        user_commission = data.get('predicted_user_commission')
        if user_commission:
            user_commission = Commission.from_api_data(user_commission)

        kwargs = {
            'code': data.get('discount_code'),
            'description': data.get('discount_desc'),
            'disallowed_seat_nos': data.get('discount_disallowed_seat_nos'),
            'price_band_code': data.get('price_band_code'),
            'is_offer': data.get('is_offer', False),
            'seatprice': data.get('sale_seatprice'),
            'surcharge': data.get('sale_surcharge'),
            'non_offer_seatprice': data.get('non_offer_sale_seatprice'),
            'non_offer_surcharge': data.get('non_offer_sale_surcharge'),
            'availability': data.get('number_available'),
            'percentage_saving': data.get('percentage_saving'),
            'absolute_saving': data.get('absolute_saving'),
            'gross_commission': gross_commission,
            'user_commission': user_commission,
            'semantic_type': data.get('discount_semantic_type'),
            'minimum_eligible_age': data.get('discount_minimum_eligible_age'),
            'maximum_eligible_age': data.get('discount_maximum_eligible_age'),
        }

        tax_component = data.get('sale_combined_tax_component')
        if tax_component is not None:
            kwargs.update(tax_component=tax_component)

        kwargs.update(SeatPricingMixin.kwargs_from_api_data(data))

        return cls(**kwargs)

    def __repr__(self):
        return u'<Discount {}:{}>'.format(
            self.code, self.description.encode('ascii', 'ignore')
        )
