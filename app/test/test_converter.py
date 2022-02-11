from app.core.converter.bitcoin_converter import CexBitcoinConverter


def test_should_return_none() -> None:
    converter = CexBitcoinConverter()
    assert converter.convert_btc_to("ussssd", 12) is None


def test_should_return_float() -> None:
    converter = CexBitcoinConverter()
    assert type(converter.convert_btc_to("USD", 12)) is float
    assert type(converter.convert_btc_to("EUR", 12)) is float
