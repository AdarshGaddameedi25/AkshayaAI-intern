from db_config import stocks_collection


stocks_data = list(
    stocks_collection.find({"stock": "TSLA"}).sort("date", 1)
)

for i in range(1, len(stocks_data)):

    previous_close = stocks_data[i - 1]["close"]
    current_close = stocks_data[i]["close"]

    
    daily_return = (
        (current_close - previous_close)
        / previous_close
    ) * 100

    
    stocks_collection.update_one(
        {"_id": stocks_data[i]["_id"]},
        {"$set": {"daily_return": daily_return}}
    )

print("Daily returns calculated successfully!")