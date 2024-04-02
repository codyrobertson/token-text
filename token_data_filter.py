def filter_token_data(token_data):
    filtered_data = {}

    if 'current_data' in token_data:
        current_data = token_data['current_data']
        filtered_data['id'] = current_data.get('id')
        filtered_data['symbol'] = current_data.get('symbol')
        filtered_data['name'] = current_data.get('name')
        filtered_data['current_price'] = current_data.get('market_data', {}).get('current_price', {}).get('usd')
        filtered_data['price_change_percentage_24h'] = current_data.get('market_data', {}).get('price_change_percentage_24h')
        filtered_data['market_cap'] = current_data.get('market_data', {}).get('market_cap', {}).get('usd')
        filtered_data['total_volume'] = current_data.get('market_data', {}).get('total_volume', {}).get('usd')

    if 'tickers' in token_data:
        tickers = token_data['tickers']
        
        # Sort tickers by volume in descending order, handling None values
        sorted_tickers = sorted(tickers, key=lambda x: x['converted_volume']['usd'] if x['converted_volume']['usd'] is not None else -1, reverse=True)
        
        # Get the top 3 exchanges by volume
        top_exchanges = [exchange['market']['name'] for exchange in sorted_tickers[:3] if 'market' in exchange]
        filtered_data['exchanges'] = top_exchanges
        
        # Get the top 3 pairs by volume
        top_pairs = [f"{ticker['base']}/{ticker['target']}" for ticker in sorted_tickers[:3]]
        filtered_data['pairs'] = top_pairs

    return filtered_data
