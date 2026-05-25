from flask import Flask, render_template
import os

import pandas as pd

from db_config import stocks_collection
from ml_model import run_prediction_workflow
from prediction_graph import save_prediction_graph


app = Flask(__name__)

EXPECTED_COLUMNS = [
    "stock",
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "daily_return",
]


def get_stock_table(stock_symbol):
    data = list(stocks_collection.find({"stock": stock_symbol}))
    df = pd.DataFrame(data)

    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            df[column] = None

    if not df.empty:
        df = df[EXPECTED_COLUMNS]
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    return df


def render_stock_page(stock_symbol):
    df = get_stock_table(stock_symbol)
    table_data = df.tail(20).to_html(index=False) if not df.empty else "<p>No stock data available.</p>"

    return render_template(
        "stock.html",
        stock_name=stock_symbol,
        table=table_data,
        prediction_url=f"/prediction/{stock_symbol.lower()}"
    )


def render_prediction_page(stock_symbol):
    result = run_prediction_workflow(stock_symbol)

    if result.get("error"):
        return render_template(
            "prediction.html",
            stock_name=stock_symbol,
            error=result["error"],
            prediction_url=f"/prediction/{stock_symbol.lower()}"
        )

    graph_name = f"{stock_symbol.lower()}_prediction_graph.png"
    graph_path = os.path.join("static", graph_name)
    save_prediction_graph(
        stock_symbol,
        result["dates"],
        result["actual_values"],
        result["predicted_values"],
        graph_path,
    )

    return render_template(
        "prediction.html",
        stock_name=stock_symbol,
        graph_file=graph_name,
        metrics=result["metrics"],
        next_day_predictions=result["next_day_predictions"],
        best_model=result["best_model"],
        best_prediction=round(result["best_prediction"], 2),
        prediction_url=f"/prediction/{stock_symbol.lower()}"
    )


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tsla')
def tsla():
    return render_stock_page("TSLA")


@app.route('/aapl')
def aapl():
    return render_stock_page("AAPL")


@app.route('/msft')
def msft():
    return render_stock_page("MSFT")


@app.route('/prediction/tsla')
def prediction_tsla():
    return render_prediction_page("TSLA")


@app.route('/prediction/aapl')
def prediction_aapl():
    return render_prediction_page("AAPL")


@app.route('/prediction/msft')
def prediction_msft():
    return render_prediction_page("MSFT")


if __name__ == '__main__':
    app.run(debug=True)