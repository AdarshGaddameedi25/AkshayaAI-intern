import yfinance as yf
import pandas as pd
from db_config import stocks_collection


stocks = ["TSLA", "AAPL", "MSFT"]

for stock in stocks:

    print(f"\nFetching {stock} data...\n")


    ticker = yf.Ticker(stock)

    df = ticker.history(period="1mo")

    df["daily_return"] = df["Close"].pct_change() * 100

    df.reset_index(inplace=True)

    for index, row in df.iterrows():

        daily = row.get("daily_return")
        if pd.isna(daily):
            daily_val = None
        else:
            daily_val = float(daily)

        stock_data = {
            "stock": stock,
            "date": str(row["Date"]),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
            "daily_return": daily_val
        }

        stocks_collection.insert_one(stock_data)

    print(f"{stock} data stored successfully!")