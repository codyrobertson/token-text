import json
from .token_id import TokenMatcher
from pycoingecko import CoinGeckoAPI

class TokenPriceInfo:
    def __init__(self, token_identifier):
        self.token_identifier = token_identifier
        self.cg_api = CoinGeckoAPI()
        self.token_matcher = TokenMatcher()

    async def fetch_token_price_info(self):
        matched_token = await self.token_matcher.find_token(self.token_identifier)
        if not matched_token:
            print(f"No match found for token identifier: {self.token_identifier}")
            return None

        token_id = matched_token.get('api_id')
        if not token_id:
            print(f"No CoinGecko ID found for token identifier: {self.token_identifier}")
            return None

        try:
            token_data = self.cg_api.get_coin_by_id(id=token_id)
        except ValueError as e:
            if "404" in str(e):
                print(f"Token not found on CoinGecko: {token_id}")
            else:
                print(f"Error fetching data for token: {token_id}. Error: {e}")
            return None

        if not token_data:
            print(f"No data found for token: {token_id}")
            return None

        price_info = self.extract_price_info(token_data)

        return price_info

    @staticmethod
    def extract_price_info(token_data):
        market_data = token_data.get('market_data', {})
        price_info = {
            'current_price': market_data.get('current_price', {}).get('usd', 'N/A'),
            'price_change_percentage_1h_in_currency': market_data.get('price_change_percentage_1h_in_currency', {}).get('usd', 'N/A'),
            'price_change_percentage_24h_in_currency': market_data.get('price_change_percentage_24h_in_currency', {}).get('usd', 'N/A'),
            'price_change_percentage_7d_in_currency': market_data.get('price_change_percentage_7d_in_currency', {}).get('usd', 'N/A'),
            'market_cap': market_data.get('market_cap', {}).get('usd', 'N/A'),
            'total_volume': market_data.get('total_volume', {}).get('usd', 'N/A')
        }
        return price_info

    def export_price_info(self, price_info):
        if price_info:
            with open('token_price_info.json', 'w') as f:
                json.dump(price_info, f)
            print("Token price info exported to token_price_info.json")
        else:
            print("No price info to export.")
