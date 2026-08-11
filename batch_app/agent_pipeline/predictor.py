import pickle
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from catboost import CatBoostClassifier

BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from utils.feature_engineering import create_engineered_features

MODEL_PATH = BASE_DIR / "models" / "catboost_readmission_model.cbm"
THRESHOLD_PATH = BASE_DIR / "models" / "best_threshold.pkl"
FEATURE_ORDER_PKL = BASE_DIR / "models" / "feature_order.pkl"
FEATURE_ORDER_CSV = BASE_DIR / "models" / "feature_order.csv"

DEFAULT_THRESHOLD = 0.18

FEATURE_ENGINEERING_REQUIRED_COLUMNS = [
    "num_procedures",
    "los_days",
    "total_cost_inr",
    "govt_subsidy_inr",
    "out_of_pocket_inr",
    "charlson_index",
    "comorbidity_count",
    "age"
]


def load_threshold():
    if not THRESHOLD_PATH.exists():
        return DEFAULT_THRESHOLD

    with open(THRESHOLD_PATH, "rb") as f:
        threshold_object = pickle.load(f)

    if isinstance(threshold_object, dict):
        for key in ["threshold", "best_threshold", "value"]:
            if key in threshold_object:
                return float(threshold_object[key])

        for value in threshold_object.values():
            try:
                return float(value)
            except Exception:
                continue

    if isinstance(threshold_object, (list, tuple)):
        return float(threshold_object[0])

    return float(threshold_object)


def load_feature_order():
    if FEATURE_ORDER_PKL.exists():
        with open(FEATURE_ORDER_PKL, "rb") as f:
            feature_order_object = pickle.load(f)

        if isinstance(feature_order_object, list):
            return feature_order_object

        if isinstance(feature_order_object, np.ndarray):
            return feature_order_object.tolist()

        if isinstance(feature_order_object, pd.DataFrame):
            return feature_order_object.iloc[:, 0].astype(str).tolist()

        if isinstance(feature_order_object, pd.Series):
            return feature_order_object.astype(str).tolist()

    if FEATURE_ORDER_CSV.exists():
        feature_df = pd.read_csv(FEATURE_ORDER_CSV)

        if len(feature_df.columns) == 1:
            return feature_df.iloc[:, 0].astype(str).tolist()

        return feature_df.columns.tolist()

    return None


def load_model():
    model = CatBoostClassifier()
    model.load_model(MODEL_PATH)
    return model


def ensure_columns(df, feature_order):
    for col in feature_order:
        if col not in df.columns:
            df[col] = np.nan

    return df[feature_order]


def prepare_categorical_columns(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("Unknown").astype(str)

    return df


def predict_batch(df, model=None, threshold=None, feature_order=None):
    df = df.copy().reset_index(drop=True)

    report = {
        "rows_input": len(df),
        "rows_predicted": 0,
        "rows_with_actual_outcome": 0,
        "high_risk_predicted": 0,
        "threshold": None,
        "messages": []
    }

    if len(df) == 0:
        report["messages"].append("Input dataframe is empty.")
        return df, report

    if "readmitted_30d" in df.columns:
        actual = pd.to_numeric(df["readmitted_30d"], errors="coerce")
    else:
        actual = pd.Series(np.nan, index=df.index)

    missing_mask = actual.isna()
    known_mask = actual.notna()

    df["label_available"] = known_mask.astype(bool)
    df["predicted_probability"] = pd.Series(np.nan, index=df.index, dtype="float64")
    df["predicted_readmission_30d"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
    df["prediction_status"] = pd.Series(None, index=df.index, dtype="object")

    df.loc[known_mask, "prediction_status"] = "actual_known"

    report["rows_with_actual_outcome"] = int(known_mask.sum())

    if threshold is None:
        threshold = load_threshold()

    report["threshold"] = threshold

    if feature_order is None:
        feature_order = load_feature_order()

    if feature_order is None:
        raise ValueError("feature_order file not found.")

    if "readmitted_30d" in feature_order:
        feature_order.remove("readmitted_30d")

    for col in FEATURE_ENGINEERING_REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    feature_df = create_engineered_features(df)

    feature_df = ensure_columns(feature_df, feature_order)

    feature_df = prepare_categorical_columns(feature_df)

    if model is None:
        model = load_model()

    probabilities = model.predict_proba(feature_df)[:, 1]

    df["predicted_probability"] = probabilities

    if missing_mask.any():
        df.loc[missing_mask, "predicted_readmission_30d"] = (
            df.loc[missing_mask, "predicted_probability"] >= threshold
        ).astype("Int64")

        df.loc[missing_mask, "prediction_status"] = "predicted"

        report["rows_predicted"] = int(missing_mask.sum())

        report["high_risk_predicted"] = int(
            df.loc[missing_mask, "predicted_readmission_30d"].sum()
        )

        report["messages"].append(
            f"Prediction completed for {report['rows_predicted']} rows."
        )

    else:
        report["rows_predicted"] = 0
        report["high_risk_predicted"] = 0

        report["messages"].append(
            "No blank readmitted_30d rows found. Probabilities computed for evaluation only."
        )

    return df, report