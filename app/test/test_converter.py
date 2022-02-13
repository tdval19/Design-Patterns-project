import pytest

from app.core.converter.bitcoin_converter import CexBitcoinConverter, IBitcoinConverter


@pytest.fixture
def converter() -> IBitcoinConverter:
    return CexBitcoinConverter()


class TestBitcoinConverter:
    def test_should_return_none(self, converter: IBitcoinConverter) -> None:
        assert converter.convert_btc_to("ussssd", 12) is None

    def test_should_return_float(self, converter: IBitcoinConverter) -> None:
        assert type(converter.convert_btc_to("USD", 12)) is float
        assert type(converter.convert_btc_to("EUR", 12)) is float
