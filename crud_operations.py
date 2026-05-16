print("READ Operation:\n")

results = stocks_collection.find({"stock": "TSLA"})

for data in results:
    print(data) 

print("\nUPDATE Operation\n")

stocks_collection.update_one(
    {"stock": "TSLA"},
    {"$set": {"market": "NASDAQ"}}
)

print("DELETE Operation!\n")

stocks_collection.delete_one(
    {"stock": "TSLA"}
)

