"""Shared type aliases."""

from decimal import Decimal
from typing import TypeAlias

# The API returns JSON numbers, which are parsed as ``float`` by default or as
# ``Decimal`` when the client is created with ``use_decimal=True``.
Number: TypeAlias = float | Decimal
