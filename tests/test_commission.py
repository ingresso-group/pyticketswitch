from pyticketswitch.commission import Commission


class TestCommission:

    def test_from_api_data(self):

        data = {
            "amount_excluding_vat": 2.93,
            "amount_including_vat": 3.51,
            "commission_currency_code": "gbp",
        }

        commission = Commission.from_api_data(data)

        assert commission.including_vat == 3.51
        assert commission.excluding_vat == 2.93
        assert commission.currency_code == 'gbp'
