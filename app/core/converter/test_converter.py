from app.core.converter.bitcoin_converter import CexBitcoinConverter


def test_should_return_none() -> None:
    converter = CexBitcoinConverter()
    assert converter.convert_btc_to("ussssd") is None


def test_should_return_float() -> None:
    converter = CexBitcoinConverter()
    assert type(converter.convert_btc_to("USD")) is float
    assert type(converter.convert_btc_to("EUR")) is float
