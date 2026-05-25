from db_config import stocks_collection

stocks = ["TSLA", "AAPL", "MSFT"]

for stock in stocks:

    stocks_data = list(
        stocks_collection.find({"stock": stock}).sort("date", 1)
    )

   
    for i in range(1, len(stocks_data)):

        previous_close = stocks_data[i - 1]["close"]
        current_close = stocks_data[i]["close"]

        # Calculate daily return
        daily_return = (
            (current_close - previous_close)
            / previous_close
        ) * 100

        # Update MongoDB document
        stocks_collection.update_one(
            {"_id": stocks_data[i]["_id"]},
            {"$set": {"daily_return": daily_return}}
        )

    print(f"{stock} returns calculated successfully!")