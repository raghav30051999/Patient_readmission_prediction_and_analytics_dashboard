import numpy as np
import pandas as pd

from agent_pipeline.data_cleaner import clean_batch
from agent_pipeline.predictor import predict_batch
from agent_pipeline.evaluator import evaluate_batch


def run_fair_evaluation(df, mask_ratio=0.5, seed=42):
    df = df[df["readmitted_30d"].notna()].copy()
    df = df.reset_index(drop=True)

    np.random.seed(seed)
    mask = np.random.rand(len(df)) < mask_ratio

    true_values = df.loc[mask, "readmitted_30d"].copy()

    df.loc[mask, "readmitted_30d"] = np.nan

    cleaned_df, cleaning_report = clean_batch(df)

    predicted_df, prediction_report = predict_batch(cleaned_df)

    eval_df = predicted_df.loc[mask].copy()
    eval_df["readmitted_30d"] = true_values
    eval_df["label_available"] = True

    evaluation_report, evaluated_df = evaluate_batch(eval_df)

    summary = {
        "total_rows": len(df),
        "masked_rows": int(mask.sum()),
        "known_rows": int((~mask).sum()),
        "rows_predicted": prediction_report["rows_predicted"]
    }

    return evaluation_report, evaluated_df, summary