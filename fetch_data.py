import yfinance as yf
import pandas as pd 

stocks=["TSLA","AAPL","MSFT"]
for stock in stocks:
    print(f"\nFetching data for {stock}...\n")

    ticker = yf.Ticker(stock)

    df = ticker.history(period="1mo")

    filename = f"{stock}.csv"

    df.to_csv(filename)

    print(f"{stock} saved successfully!") 
