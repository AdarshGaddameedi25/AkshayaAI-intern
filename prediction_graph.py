import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def save_prediction_graph(stock_symbol, dates, actual_values, predicted_values, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(dates, actual_values, label="Actual", marker="o", linewidth=2)

    for model_name, model_predictions in predicted_values.items():
        plt.plot(dates, model_predictions, label=model_name, marker="o", linewidth=1.5)

    plt.title(f"{stock_symbol} Actual vs Predicted Close Prices")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()