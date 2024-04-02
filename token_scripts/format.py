def format_number(number):
    """
    Format numbers with commas and shorten them using units like K, M, B, T.
    """
    if number < 1000:
        return str(number)
    elif 1000 <= number < 1000000:
        return f"{round(number/1000, 2)}K"
    elif 1000000 <= number < 1000000000:
        return f"{round(number/1000000, 2)}M"
    elif 1000000000 <= number < 1000000000000:
        return f"{round(number/1000000000, 2)}B"
    else:
        return f"{round(number/1000000000000, 2)}T"

def format_cg(output_list):
    price, change, token_id = output_list
    formatted_price = format_number(price)
    output = f"```{token_id.upper()} ${formatted_price} ({str(change)}% 24h)```"
    return output

def format_historical_cg(output, date, token_id):
    formatted_output = format_number(round(output, 2))
    output = f"```{token_id} was ${formatted_output} on {date}```"
    return output

def format_conversion(output):
    formatted_output = format_number(round(output, 2))
    output = f"```{formatted_output}```"
    return output

def format_price_change_percentage(change):
    """
    Format price change percentage with up/down emojis.
    """
    if change > 0:
        emoji = "🔼" if change < 5 else "⏫"
    else:
        emoji = "🔽"
    return f"{change}% {emoji}"

def format_market_data(price_change_percentage, market_cap, trading_volume):
    formatted_market_cap = format_number(market_cap)
    formatted_trading_volume = format_number(trading_volume)
    formatted_changes = {period: format_price_change_percentage(change) for period, change in price_change_percentage.items()}
    return f"Market Cap: ${formatted_market_cap}, Trading Volume: ${formatted_trading_volume}, Price Changes: {formatted_changes}"
