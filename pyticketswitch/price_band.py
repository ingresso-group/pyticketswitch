from pyticketswitch.cost_range import CostRange
from pyticketswitch.discount import Discount


class PriceBand(object):

    def __init__(self, code, default_discount, description=None,
                 cost_range=None, no_singles_cost_range=None):

        self.code = code
        self.description = description
        self.cost_range = cost_range
        self.no_singles_cost_range = no_singles_cost_range
        self.default_discount = default_discount

    @classmethod
    def from_api_data(cls, data):
        api_cost_range = data.get('cost_range', {})
        api_no_singles_cost_range = api_cost_range.get('no_singles_cost_range', {})
        cost_range = None
        no_singles_cost_range = None

        if api_cost_range:
            api_cost_range['singles'] = True
            cost_range = CostRange.from_api_data(api_cost_range)

        if api_no_singles_cost_range:
            api_no_singles_cost_range['singles'] = False
            no_singles_cost_range = CostRange.from_api_data(
                api_no_singles_cost_range)

        discount = Discount.from_api_data(data)

        kwargs = {
            'code': data.get('price_band_code', None),
            'description': data.get('price_band_desc', None),
            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
            'default_discount': discount,
        }

        return cls(**kwargs)
