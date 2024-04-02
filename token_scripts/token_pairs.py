import json
import asyncio
from .token_id import TokenMatcher
from pycoingecko import CoinGeckoAPI

class TokenTradingInfo:
    def __init__(self, token_name):
        self.token_name = token_name
        self.cg_api = CoinGeckoAPI()
        self.token_matcher = TokenMatcher()

    async def fetch_trading_info(self):
        matched_token = await self.token_matcher.find_token(self.token_name)
        if not matched_token:
            print(f"No match found for token: {self.token_name}")
            return None

        symbol = matched_token.get('symbol')
        if not symbol:
            print(f"No symbol found for token: {self.token_name}")
            return None

        try:
            token_data = self.cg_api.get_coin_by_id(id=matched_token['id'])
        except Exception as e:
            print(f"Failed to fetch data for token: {symbol}. Error: {e}")
            return None

        if not token_data:
            print(f"No data found for token: {symbol}")
            return None

        # Extracting 3 most popular trading pairs
        trading_pairs = token_data.get('tickers', [])[:3]
        popular_trading_pairs = [{
            'base': pair.get('base'),
            'target': pair.get('target'),
            'volume': pair.get('volume')
        } for pair in trading_pairs]

        # Extracting 3 most popular exchanges
        popular_exchanges = [{
            'name': exchange.get('market', {}).get('name'),
            'trade_volume_24h_btc': exchange.get('market', {}).get('trade_volume_24h_btc')
        } for exchange in trading_pairs]  # Reuse trading_pairs as it contains exchange info

        return {
            'popular_trading_pairs': popular_trading_pairs,
            'popular_exchanges': popular_exchanges
        }

    def export_trading_info(self, trading_info):
        if trading_info:
            with open('token_trading_info.json', 'w') as f:
                json.dump(trading_info, f)
            print("Token trading info exported to token_trading_info.json")
        else:
            print("No trading info to export.")
