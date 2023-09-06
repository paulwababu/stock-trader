from concurrent.futures import ThreadPoolExecutor
import time
import redis
import alpaca_trade_api as tradeapi

# Initialize Alpaca API
SEC_KEY = 'YOUR_SECRET_KEY'
PUB_KEY = 'YOUR_PUBLIC_KEY'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

# Initialize
currency_pairs = ['USD/EUR', 'USD/GBP', 'USD/JPY']  # Make sure these pairs are available on Alpaca
exchanges = ['Alpaca']
threshold_profit_margin = 0.01
trading_capital = 10.0
pool = ThreadPoolExecutor(max_workers=10)

# Initialize Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Function to get prices using Alpaca API
def get_price(exchange, pair):
    market_data = api.get_barset(pair, 'minute', limit=1)
    close_price = market_data[pair][0].c
    # Assuming a 0.02 spread between buy and sell for simplicity
    return close_price - 0.01, close_price + 0.01

# Function to simulate executing a trade
def execute_trade(buy_exchange, sell_exchange, pair):
    print(f"Executed trade: Bought {pair} from {buy_exchange} and sold on {sell_exchange}")

# Function to populate Redis with data
def fetch_data(pair):
    for exchange in exchanges:
        buy_price, sell_price = get_price(exchange, pair)
        r.hset(pair, f"{exchange}_buy", buy_price)
        r.hset(pair, f"{exchange}_sell", sell_price)

# Main trading logic
def main():
    while True:
        for pair in currency_pairs:
            lowest_buy_price = float('inf')
            highest_sell_price = 0.0
            buy_exchange = ''
            sell_exchange = ''
            
            for exchange in exchanges:
                buy_price = float(r.hget(pair, f"{exchange}_buy"))
                sell_price = float(r.hget(pair, f"{exchange}_sell"))

                if buy_price < lowest_buy_price:
                    lowest_buy_price = buy_price
                    buy_exchange = exchange
                
                if sell_price > highest_sell_price:
                    highest_sell_price = sell_price
                    sell_exchange = exchange
            
            potential_profit = highest_sell_price - lowest_buy_price - 0.002  # Assume 0.002 as transaction fee
            
            if potential_profit > threshold_profit_margin:
                execute_trade(buy_exchange, sell_exchange, pair)
                trading_capital += potential_profit

        time.sleep(60)  # Repeat every minute

# Fetch data using threads
with ThreadPoolExecutor(max_workers=len(currency_pairs)) as executor:
    executor.map(fetch_data, currency_pairs)

# Run main trading logic
main()
