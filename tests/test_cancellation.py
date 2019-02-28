import json
import pytest

from pyticketswitch.cancellation import CancellationResult


class TestCancellationResult:
    def test_from_api_data_successful_cancellation(self):
        with open("test_data/successful_cancellation.json", 'r') as file_handle:
            data = json.load(file_handle)
        cancellation_result = CancellationResult.from_api_data(data)

        assert cancellation_result.cancelled_item_numbers == [1]
        assert len(cancellation_result.trolley.bundles) == 1
        assert len(cancellation_result.trolley.bundles[0].orders) == 1
        assert cancellation_result.must_also_cancel is None

    def test_from_api_data_must_also_cancel(self):
        with open("test_data/must_also_cancel_cancellation.json", 'r') as file_handle:
            data = json.load(file_handle)
        cancellation_result = CancellationResult.from_api_data(data)

        assert len(cancellation_result.cancelled_item_numbers) == 0
        assert len(cancellation_result.trolley.bundles) == 0
        assert len(cancellation_result.must_also_cancel) == 1
        assert cancellation_result.must_also_cancel[0].item == 2

    @pytest.mark.parametrize(
        "cancellation_data_file,expected_result",
        [
            ("test_data/successful_cancellation.json", True),
            ("test_data/must_also_cancel_cancellation.json", False),
            ("test_data/partial_cancellation.json", False),
            ("test_data/failed_cancellation.json", False),
        ],
    )
    def test_is_fully_cancelled(self, cancellation_data_file, expected_result):
        with open(cancellation_data_file, 'r') as file_handle:
            data = json.load(file_handle)
        cancellation_result = CancellationResult.from_api_data(data)

        assert cancellation_result.is_fully_cancelled() == expected_result
