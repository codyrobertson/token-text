import aiohttp
import asyncio
import time
from functools import wraps
import logging

# Setting up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rate_limited(max_per_hour):
    """
    Decorator to limit the number of API calls made to a function to avoid hitting rate limits.
    """
    min_interval = 3600.0 / float(max_per_hour)
    def decorate(func):
        last_called = [0.0]
        @wraps(func)
        async def rate_limited_function(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_for = min_interval - elapsed
            if wait_for > 0:
                await asyncio.sleep(wait_for)
            last_called[0] = time.time()
            return await func(*args, **kwargs)
        return rate_limited_function
    return decorate

def handle_api_exceptions(func):
    """
    Decorator to handle exceptions for API requests.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientError as e:
            logging.error(f"Client exception occurred: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None
    return wrapper

class APIRequestHandler:
    """
    A utility class for handling API requests, logging, and error handling.
    """
    @staticmethod
    @handle_api_exceptions
    @rate_limited(100)  # Assuming a generic rate limit of 100 requests per hour
    async def make_request(url, params=None):
        """
        Make an asynchronous HTTP request to a specified URL with optional parameters.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f"Failed to fetch data: {response.status} - {await response.text()}")
                    return None

# Example usage
if __name__ == "__main__":
    async def main():
        handler = APIRequestHandler()
        url = "https://api.coingecko.com/api/v3/ping"
        result = await handler.make_request(url)
        if result:
            logging.info("API is up and running.")
        else:
            logging.error("Failed to reach the API.")
    
    asyncio.run(main())

