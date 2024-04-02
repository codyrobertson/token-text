import asyncio
import argparse
import json
import uuid
from token_scripts.token_id import TokenMatcher
from token_scripts.token_pairs import TokenTradingInfo
from token_scripts.token_price import TokenPriceInfo
from token_scripts.format import format_market_data
from token_scripts.charting import get_chart
from token_scripts.suggest_token import TokenSuggestion

async def main(token_name):
    # Suggest tokens based on the input
    token_suggestion = TokenSuggestion('tokens_list.json')
    suggestions = await token_suggestion.suggest_tokens(token_name)
    suggestions = json.loads(suggestions)
    
    if not suggestions:
        print(f"No suggestions found for token: {token_name}")
        return
    
    # Display suggestions
    for i, suggestion in enumerate(suggestions, start=1):
        print(f"{i}. {suggestion['name']} ({suggestion['symbol']})")
    
    # User selects a suggestion
    selection = int(input("Enter the number of the token you wish to select: ")) - 1
    selected_token = suggestions[selection]
    token_name = selected_token['name']
    
    # Save the selection for learning
    unique_id = str(uuid.uuid4())
    with open(f'results/selected_token_{unique_id}.json', 'w') as file:
        json.dump(selected_token, file, indent=4)
    
    # Fetch token ID and symbol
    token_matcher = TokenMatcher()
    matched_token = await token_matcher.find_token(token_name)
    if not matched_token:
        print(f"No match found for token: {token_name}")
        return

    # Fetch trading info
    trading_info = TokenTradingInfo(token_name)
    try:
        trading_data = await trading_info.fetch_trading_info()
        if trading_data:
            trading_info.export_trading_info(trading_data)
        else:
            print("Failed to fetch trading info.")
    except ValueError as e:
        print(f"Failed to fetch data for token: {token_name}. Error: {e}")

    # Refactored section to fetch and process price info
    async def fetch_and_process_price_info(token_name):
        price_info = TokenPriceInfo(token_name)
        price_data = await price_info.fetch_token_price_info()
        if price_data:
            price_info.export_price_info(price_data)
            price_change_percentage = {
                '1h': price_data['price_change_percentage_1h_in_currency'],
                '24h': price_data['price_change_percentage_24h_in_currency'],
                '7d': price_data['price_change_percentage_7d_in_currency']
            }
            market_cap = price_data['market_cap']
            trading_volume = price_data['total_volume']
            formatted_market_data = format_market_data(price_change_percentage, market_cap, trading_volume)
            print(f"Market Data: {formatted_market_data}")
        else:
            print("Failed to fetch price info.")
    
    await fetch_and_process_price_info(token_name)

    # Generate chart
    if matched_token:
        symbol = matched_token['symbol']
        chart_path = get_chart(symbol, '1y', '1d')
        print(f"Chart saved at: {chart_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and display token information.')
    parser.add_argument('token_name', type=str, help='The name of the token to fetch information for.')
    args = parser.parse_args()

    asyncio.run(main(args.token_name))
