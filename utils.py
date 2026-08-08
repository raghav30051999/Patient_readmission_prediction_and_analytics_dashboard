import joblib
from catboost import CatBoostClassifier
import pandas as pd

# ----------------------------------------
# Load Model
# ----------------------------------------

def load_model():

    model = CatBoostClassifier()

    model.load_model("catboost_readmission_model.cbm")

    return model


# ----------------------------------------
# Load Threshold
# ----------------------------------------

def load_threshold():

    return joblib.load("best_threshold.pkl")


# ----------------------------------------
# Load Feature Order
# ----------------------------------------

def load_feature_order():

    return joblib.load("feature_order.pkl")


# ----------------------------------------
# Load Model Information
# ----------------------------------------

def load_model_info():

    return joblib.load("model_info.pkl")


# ----------------------------------------
# Predict
# ----------------------------------------

def predict(model, X, threshold):

    probabilities = model.predict_proba(X)[:, 1]

    predictions = (probabilities >= threshold).astype(int)

    return predictions, probabilities


# ----------------------------------------
# Risk Level
# ----------------------------------------

def risk_level(probability):

    if probability < 0.30:
        return "Low"

    elif probability < 0.60:
        return "Moderate"

    else:
        return "High"