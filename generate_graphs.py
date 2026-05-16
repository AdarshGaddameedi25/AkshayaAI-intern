import matplotlib.pyplot as plt
import pandas as pd
from db_config import stocks_collection


stocks = ["TSLA", "AAPL", "MSFT"]

for stock in stocks:

    data = list(
        stocks_collection.find({"stock": stock})
    )


    df = pd.DataFrame(data)


    df = df.sort_values("date")

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["date"],
        df["close"],
        marker='o'
    )

    plt.title(f"{stock} Closing Prices")

    plt.xlabel("Date")
    plt.ylabel("Close Price")

    plt.xticks(rotation=45)

    plt.tight_layout()

    # Save graph image
    plt.savefig(
        f"static/{stock.lower()}_graph.png"
    )

    plt.close()

print("Graphs generated successfully!")