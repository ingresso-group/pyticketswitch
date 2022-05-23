from pyticketswitch.purchase_result import PurchaseResult


class TestPurchaseResult:

    def test_from_api_data(self):

        data = {
            "failed_3d_secure": True,
            "failed_avs": True,
            "failed_cv_two": True,
            "purchase_error": "too much donk",
            "success": True,
            "failure_reason": "unknown",
            "internal_error_comment": "Even more error info",
            "is_partial": True,
            "is_semi_credit": False,
        }

        purchase_result = PurchaseResult.from_api_data(data)

        assert purchase_result.success is True
        assert purchase_result.failed_3d_secure is True
        assert purchase_result.failed_avs is True
        assert purchase_result.failed_cv_two is True
        assert purchase_result.error == 'too much donk'
        assert purchase_result.failure_reason == 'unknown'
        assert purchase_result.internal_error_comment == 'Even more error info'
        assert purchase_result.is_partial
        assert not purchase_result.is_semi_credit
