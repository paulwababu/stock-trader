# Arbitrage Trading Bot

## Description

This is a simple arbitrage trading bot written in Python. The bot aims to identify arbitrage opportunities in different currency pairs over various exchanges and execute trades to capitalize on the price differentials.

## Trading Strategy

1. **Data Gathering**: The bot fetches real-time price data for different currency pairs like USD/EUR, USD/GBP, etc., from Alpaca's API.
2. **Storage**: The fetched data is stored in a Redis database for quick retrieval.
3. **Arbitrage Identification**: For each currency pair, the bot identifies the exchange with the lowest buying price and the exchange with the highest selling price.
4. **Profit Calculation**: The bot calculates the potential profit from each arbitrage opportunity.
5. **Trade Execution**: If the potential profit is above a predefined threshold, the bot executes the trade.

## Pre-requisites

- Python 3.x
- Redis
- Alpaca account and API keys

## Installation

1. Clone the repository.
    ```
    git clone https://github.com/yourusername/arbitrage-bot.git
    ```
2. Install the required packages.
    ```
    pip install -r requirements.txt
    ```

## How to Run

1. Start the Redis server.
    ```
    redis-server
    ```

2. Replace the placeholder Alpaca API keys (`PUB_KEY`, `SEC_KEY`) with your actual keys.

3. Run the Python script.
    ```
    python arbitrage_bot.py
    ```

**Note**: Before running the bot with real money, make sure to test extensively and understand the associated risks.