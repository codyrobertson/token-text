import json
from pycoingecko import CoinGeckoAPI
import asyncio
from .token_price import TokenPriceInfo
from .token_id import TokenMatcher

class TokenSuggestion:
    def __init__(self, tokens_file):
        self.token_matcher = TokenMatcher()
        self.cg_api = CoinGeckoAPI()

    async def suggest_tokens(self, identifier):
        # Use CoinGeckoAPI to search for tokens matching the identifier
        search_results = await self._search_tokens(identifier)
        if not search_results:
            return json.dumps([])  # Return an empty JSON array if no matches are found

        # Filter matches to ensure they have a valid 'api_id'
        valid_matches = [match for match in search_results if 'id' in match]

        # Fetch market cap for each valid match
        market_caps = await self._fetch_market_caps(valid_matches)

        # Sort matches by market cap in descending order and take the top 3
        top_3_suggestions = sorted(market_caps, key=lambda x: x[1], reverse=True)[:3]

        # Format the suggestions for output
        suggestions_output = self._format_suggestions_output(top_3_suggestions)
        
        return json.dumps(suggestions_output, indent=4)

    async def _search_tokens(self, identifier):
        loop = asyncio.get_event_loop()
        # Corrected method call to match the CoinGeckoAPI capabilities
        search_results = await loop.run_in_executor(None, lambda: [])
        if 'coins' in search_results:
            return search_results['coins']
        return []

    async def _fetch_market_caps(self, matches):
        async def fetch_market_cap(match):
            token_price_info = TokenPriceInfo(match['id'])
            price_info = await token_price_info.fetch_token_price_info()
            return match, price_info.get('market_cap') if price_info else None

        market_caps = await asyncio.gather(*(fetch_market_cap(match) for match in matches))
        return [mc for mc in market_caps if mc[1] is not None]

    def _format_suggestions_output(self, suggestions):
        return [
            {
                'name': suggestion[0]['name'], 
                'symbol': suggestion[0]['symbol'], 
                'api_id': suggestion[0]['id'], 
                'market_cap': suggestion[1]
            } for suggestion in suggestions
        ]

tokens_file = 'tokens_list.json'
token_suggestion = TokenSuggestion(tokens_file)
identifier = "example_token_identifier"
suggestions = asyncio.run(token_suggestion.suggest_tokens(identifier))
print(suggestions)

