from flask import Flask, render_template
import pandas as pd
from db_config import stocks_collection

app = Flask(__name__)




@app.route('/')
def home():

    return render_template('home.html')



@app.route('/tsla')
def tsla():

    data = list(
        stocks_collection.find({"stock": "TSLA"})
    )

    df = pd.DataFrame(data)
    expected_cols = [
        "stock",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "daily_return",
    ]

    for c in expected_cols:
        if c not in df.columns:
            df[c] = None

    df = df[expected_cols]

    table_data = df.tail(20).to_html()

    return render_template(
        'stock.html',
        stock_name="TSLA",
        table=table_data
    )




@app.route('/aapl')
def aapl():

    data = list(
        stocks_collection.find({"stock": "AAPL"})
    )

    df = pd.DataFrame(data)
    expected_cols = [
        "stock",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "daily_return",
    ]

    for c in expected_cols:
        if c not in df.columns:
            df[c] = None

    df = df[expected_cols]

    table_data = df.tail(20).to_html()

    return render_template(
        'stock.html',
        stock_name="AAPL",
        table=table_data
    )




@app.route('/msft')
def msft():

    data = list(
        stocks_collection.find({"stock": "MSFT"})
    )

    df = pd.DataFrame(data)
    expected_cols = [
        "stock",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "daily_return",
    ]

    for c in expected_cols:
        if c not in df.columns:
            df[c] = None

    df = df[expected_cols]

    table_data = df.tail(20).to_html()

    return render_template(
        'stock.html',
        stock_name="MSFT",
        table=table_data
    )


if __name__ == '__main__':
    app.run(debug=True)