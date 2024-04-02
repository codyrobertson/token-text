from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from CryptoPrice import Crypto
import re

app = Flask(__name__)

def check_numeric(s: str):
    pattern = r"^[+-]?[0-9]*[.]?[0-9]+$"
    return (re.match(pattern, s) is not None)

@app.route('/sms', methods=['GET', 'POST'])
async def sms_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'price' in incoming_msg:
        crypto = incoming_msg.replace('price', '').strip().upper()
        cc = Crypto(crypto)
        crypto_price = await cc.get_crypto_price()
        
        if isinstance(crypto_price, str) and not check_numeric(crypto_price):
            response = crypto_price
        else:
            response = f"The current price of {crypto} is ${crypto_price}."
        
        msg.body(response)
        responded = True
    
    elif 'data' in incoming_msg:
        crypto = incoming_msg.replace('data', '').strip().upper()
        cc = Crypto(crypto)
        crypto_data = await cc.get_crypto_data()
        
        if crypto_data:
            response = crypto_data
        else:
            response = f"Sorry, could not retrieve data for {crypto}."
        
        msg.body(response)
        responded = True
    
    elif 'chart' in incoming_msg:
        crypto, *params = incoming_msg.replace('chart', '').strip().split()
        crypto = crypto.upper()
        pair = params[0] if len(params) > 0 else 'usd'
        time_period = params[1] if len(params) > 1 else '24h'
        
        cc = Crypto(crypto)
        chart_url = await cc.get_chart(pair, time_period)
        
        if chart_url:
            response = f"Chart for {crypto} ({pair.upper()}) over {time_period}: {chart_url}"
        else:
            response = f"Sorry, could not generate chart for {crypto}."
        
        msg.body(response)
        responded = True
    
    if not responded:
        help_text = "Available commands:\n"
        help_text += "- Price <symbol>: Get the current price of a cryptocurrency\n"
        help_text += "- Data <symbol>: Get market data for a cryptocurrency\n"
        help_text += "- Chart <symbol> <pair> <time>: Generate a price chart for a cryptocurrency\n"
        msg.body(help_text)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)