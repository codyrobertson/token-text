import asyncio
import json
import os
import aiohttp

class TokenMatcher:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    async def find_token(self, identifier):
        async with aiohttp.ClientSession() as session:
            try:
                # Use CoinGecko API search endpoint to find the token
                search_url = f"{self.base_url}/search?query={identifier.lower()}"
                async with session.get(search_url) as response:
                    search_results = await response.json()
                    tokens = search_results.get('coins', [])
                    if tokens:
                        # Assuming the first result is the most relevant
                        token = tokens[0]
                        result = self.format_token_details(token['name'], token['symbol'], token['id'])
                        self.export_result(result)
                        return result
            except Exception as e:
                print(f"Error searching for token: {e}")
        return None

    def format_token_details(self, name, symbol, api_id):
        return {
            'name': name,
            'symbol': symbol,
            'api_id': api_id
        }

    def export_result(self, result):
        if result is not None:
            os.makedirs('results', exist_ok=True)
            with open('results/matched_token.json', 'w') as f:
                json.dump(result, f)
            print("Result exported to results/matched_token.json")
        else:
            print("No result to export.")
