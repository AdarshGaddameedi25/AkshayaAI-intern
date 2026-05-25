import math

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor

from db_config import stocks_collection


FEATURE_COLUMNS = [
    "open",
    "high",
    "low",
    "volume",
    "close",
    "daily_return",
]

MODEL_FACTORIES = [
    ("Linear Regression", LinearRegression),
    ("Decision Tree Regressor", DecisionTreeRegressor),
    ("Random Forest Regressor", lambda: RandomForestRegressor(n_estimators=100, random_state=42)),
]


def load_stock_data(stock_symbol):
    data = list(stocks_collection.find({"stock": stock_symbol}).sort("date", 1))
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    for column in ["date", *FEATURE_COLUMNS]:
        if column not in df.columns:
            df[column] = None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for column in FEATURE_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["date", "open", "high", "low", "close", "volume"])
    df = df.sort_values("date").reset_index(drop=True)
    df["daily_return"] = df["daily_return"].fillna(0)

    return df


def build_feature_frame(df):
    feature_frame = df.copy()
    feature_frame["target_close"] = feature_frame["close"].shift(-1)
    feature_frame = feature_frame.dropna(subset=["target_close"])
    return feature_frame


def train_and_compare_models(feature_frame):
    split_index = max(int(len(feature_frame) * 0.8), 1)
    if split_index >= len(feature_frame):
        split_index = len(feature_frame) - 1

    train_frame = feature_frame.iloc[:split_index]
    test_frame = feature_frame.iloc[split_index:]

    x_train = train_frame[FEATURE_COLUMNS]
    y_train = train_frame["target_close"]
    x_test = test_frame[FEATURE_COLUMNS]
    y_test = test_frame["target_close"]

    metrics = []
    model_predictions = {}

    for model_name, factory in MODEL_FACTORIES:
        model = factory()
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = math.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        metrics.append(
            {
                "model": model_name,
                "mae": round(float(mae), 4),
                "rmse": round(float(rmse), 4),
                "r2": round(float(r2), 4),
            }
        )
        model_predictions[model_name] = predictions.tolist()

    return metrics, model_predictions, y_test.tolist(), test_frame["date"].dt.strftime("%Y-%m-%d").tolist()


def predict_next_day_values(feature_frame, next_day_features):
    next_day_predictions = {}

    x_full = feature_frame[FEATURE_COLUMNS]
    y_full = feature_frame["target_close"]

    for model_name, factory in MODEL_FACTORIES:
        model = factory()
        model.fit(x_full, y_full)
        next_day_predictions[model_name] = round(float(model.predict(next_day_features)[0]), 2)

    return next_day_predictions


def run_prediction_workflow(stock_symbol):
    df = load_stock_data(stock_symbol)
    if df.empty or len(df) < 6:
        return {"error": f"Not enough data available for {stock_symbol} prediction."}

    feature_frame = build_feature_frame(df)
    if len(feature_frame) < 5:
        return {"error": f"Not enough usable rows available for {stock_symbol} prediction."}

    metrics, model_predictions, actual_values, dates = train_and_compare_models(feature_frame)
    next_day_features = df[FEATURE_COLUMNS].tail(1)
    next_day_predictions = predict_next_day_values(feature_frame, next_day_features)

    best_model = min(metrics, key=lambda item: item["mae"])["model"]

    print(f"\n{stock_symbol} model comparison")
    for row in metrics:
        print(f"{row['model']}: MAE={row['mae']}, RMSE={row['rmse']}, R2={row['r2']}")
    print("Next-day predictions:")
    for model_name, prediction in next_day_predictions.items():
        print(f"{model_name}: {prediction}")

    return {
        "metrics": metrics,
        "predicted_values": model_predictions,
        "actual_values": actual_values,
        "dates": dates,
        "next_day_predictions": next_day_predictions,
        "best_model": best_model,
        "best_prediction": next_day_predictions[best_model],
    }