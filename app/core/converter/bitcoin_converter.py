from typing import Optional, Protocol

import requests


class IBitcoinConverter(Protocol):
    def convert_btc_to(self, currency: str, amount_btc: float) -> Optional[float]:
        pass


class CexBitcoinConverter(IBitcoinConverter):
    api_url: str = "https://cex.io/api/last_price/BTC/"
    json_key: str = "lprice"

    def convert_btc_to(self, currency: str, amount_btc: float) -> Optional[float]:
        json = requests.get(self.api_url + currency).json()
        if self.json_key not in json:
            return None
        return amount_btc * float(
            (requests.get(self.api_url + currency).json()[self.json_key])
        )
