from pyticketswitch.cost_range import CostRange


class PriceBand(object):

    def __init__(self, code=None, description=None, cost_range=None,
                 no_singles_cost_range=None):

        self.code = code
        self.description = description
        self.cost_range = cost_range
        self.no_singles_cost_range = no_singles_cost_range
        # self.availability = availability

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

        # api_availability = data.get('avail_detail', [])
        # availability = []
        # for avail in api_availability:
        #     availability.append(AvailabilityDetails.from_api_data(avail))

        kwargs = {
            'code': data.get('price_band_code', None),
            'description': data.get('price_band_desc', None),
            'cost_range': cost_range,
            'no_singles_cost_range': no_singles_cost_range,
            # 'availability': availability,
        }

        return cls(**kwargs)
