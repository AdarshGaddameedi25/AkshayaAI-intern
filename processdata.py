import pandas as pd
import matplotlib.pyplot as plt

file_path = "TSLA.csv"
df = pd.read_csv(file_path)

df = df[["Date", "Adj Close"]]

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df["% change"] = df["Adj Close"].pct_change() * 100
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["1monthchange"] = None

for (year,month),group in df.groupby(["Year", "Month"]):
    first_price=group.iloc[0]["Adj Close"]
    last_price=group.iloc[-1]["Adj Close"]
    monthly_change = ((last_price - first_price) / first_price) * 100
    last_index = group.index[-1]
    df.loc[last_index, "1monthchange"] = monthly_change
df.to_csv("processed_tsla.csv", index=False) 
monthly_df = df.dropna(subset=["1monthchange"]).tail(24)  

plt.figure(figsize=(12, 6))
plt.plot(monthly_df["Date"], monthly_df["1monthchange"], marker='o')
plt.figure(figsize=(12, 6))
plt.plot(monthly_df["Date"], monthly_df["1monthchange"], marker='o')

plt.title("Tesla Monthly Percentage Change (Last 24 Months)")
plt.xlabel("Month")
plt.ylabel("1 Month Change (%)")
plt.xticks(rotation=45)
plt.grid(True)


plt.tight_layout()
plt.savefig("static/graph.png")

print("Processing complete!")