import yfinance as yf
import mplfinance as mpf
import pandas as pd  # Ensure pandas is imported

def fetch_ticker_history(token, period, interval):
    """
    Fetches the historical market data for a given token.
    """
    ticker = yf.Ticker(token)
    return ticker.history(period=period, interval=interval, actions=False)

def create_custom_style():
    """
    Creates a custom style for the mplfinance plot.
    """
    market_colors = mpf.make_marketcolors(up='#00bed4', down='#eb4d5c', edge='#131722', inherit=True)
    custom_style = mpf.make_mpf_style(base_mpf_style='nightclouds', facecolor='#131722', figcolor='#131722', marketcolors=market_colors)
    return custom_style

def plot_chart(data, token, style):
    """
    Plots and saves the chart based on the provided data and style.
    """
    # Check if data is empty
    if data.empty:
        print(f"No data available for {token}. Skipping chart generation.")
        return

    # Convert index to DatetimeIndex if it's not already
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)
    mpf.plot(data, title=token.upper(), type='candle', style=style, savefig=dict(fname='chart', bbox_inches='tight'))

def get_chart(token, period, interval):
    """
    High-level function to generate a chart for a given token.
    """
    history_data = fetch_ticker_history(token, period, interval)
    custom_style = create_custom_style()
    plot_chart(history_data, token, custom_style)
    return 'chart.png'

