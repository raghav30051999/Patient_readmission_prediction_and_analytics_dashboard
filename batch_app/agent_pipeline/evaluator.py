import numpy as np
import pandas as pd

from agent_pipeline.predictor import load_threshold

try:
    from sklearn.metrics import roc_auc_score, average_precision_score
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False


def safe_divide(numerator, denominator):
    if denominator == 0:
        return None
    return float(numerator) / float(denominator)


def evaluate_batch(df, threshold=None):
    report = {
        "rows_evaluated": 0,
        "rows_with_actual_outcome": 0,
        "threshold": None,
        "actual_readmission_rate": None,
        "mean_predicted_probability": None,
        "predicted_high_risk_count": None,
        "actual_readmissions_in_high_risk": None,
        "accuracy": None,
        "precision": None,
        "recall": None,
        "specificity": None,
        "f1_score": None,
        "auroc": None,
        "pr_auc": None,
        "brier_score": None,
        "confusion_matrix": {
            "true_positive": 0,
            "false_positive": 0,
            "true_negative": 0,
            "false_negative": 0
        },
        "messages": []
    }

    if threshold is None:
        threshold = load_threshold()

    report["threshold"] = threshold

    if "label_available" not in df.columns:
        report["messages"].append("label_available column not found.")
        return report, df

    if "predicted_probability" not in df.columns:
        report["messages"].append("predicted_probability column not found.")
        return report, df

    eval_df = df[
        df["label_available"] &
        df["predicted_probability"].notna()
    ].copy()

    report["rows_with_actual_outcome"] = int(df["label_available"].sum())
    report["rows_evaluated"] = len(eval_df)

    if len(eval_df) == 0:
        report["messages"].append("No rows available for evaluation.")
        return report, eval_df

    eval_df["actual_readmitted_30d"] = pd.to_numeric(
        eval_df["readmitted_30d"],
        errors="coerce"
    )

    eval_df = eval_df[eval_df["actual_readmitted_30d"].notna()].copy()

    if len(eval_df) == 0:
        report["messages"].append("No valid actual outcomes found.")
        return report, eval_df

    eval_df["actual_readmitted_30d"] = eval_df["actual_readmitted_30d"].astype(int)
    eval_df["predicted_probability"] = eval_df["predicted_probability"].astype(float)

    eval_df["predicted_readmission_at_threshold"] = (
        eval_df["predicted_probability"] >= threshold
    ).astype(int)

    actual = eval_df["actual_readmitted_30d"]
    prob = eval_df["predicted_probability"]
    pred = eval_df["predicted_readmission_at_threshold"]

    tp = int(((pred == 1) & (actual == 1)).sum())
    fp = int(((pred == 1) & (actual == 0)).sum())
    tn = int(((pred == 0) & (actual == 0)).sum())
    fn = int(((pred == 0) & (actual == 1)).sum())

    report["confusion_matrix"] = {
        "true_positive": tp,
        "false_positive": fp,
        "true_negative": tn,
        "false_negative": fn
    }

    report["actual_readmission_rate"] = safe_divide(
        int(actual.sum()),
        len(actual)
    )

    report["mean_predicted_probability"] = float(prob.mean())

    report["predicted_high_risk_count"] = int(pred.sum())

    report["actual_readmissions_in_high_risk"] = int(
        actual[pred == 1].sum()
    )

    report["accuracy"] = safe_divide(tp + tn, tp + fp + tn + fn)
    report["precision"] = safe_divide(tp, tp + fp)
    report["recall"] = safe_divide(tp, tp + fn)
    report["specificity"] = safe_divide(tn, tn + fp)

    if report["precision"] is not None and report["recall"] is not None:
        if report["precision"] + report["recall"] == 0:
            report["f1_score"] = 0.0
        else:
            report["f1_score"] = (
                2 * report["precision"] * report["recall"] /
                (report["precision"] + report["recall"])
            )

    report["brier_score"] = float(np.mean((prob - actual) ** 2))

    if SKLEARN_AVAILABLE:
        if actual.nunique() > 1:
            try:
                report["auroc"] = float(roc_auc_score(actual, prob))
            except Exception:
                report["auroc"] = None

            try:
                report["pr_auc"] = float(average_precision_score(actual, prob))
            except Exception:
                report["pr_auc"] = None
        else:
            report["messages"].append(
                "AUROC and PR-AUC not computed because only one outcome class exists in this batch."
            )
    else:
        report["messages"].append(
            "scikit-learn not available. AUROC and PR-AUC skipped."
        )

    if report["actual_readmission_rate"] is not None:
        calibration_gap = (
            report["mean_predicted_probability"] -
            report["actual_readmission_rate"]
        )

        report["calibration_gap"] = float(calibration_gap)

    report["messages"].append(
        f"Evaluation completed on {len(eval_df)} rows with actual outcomes."
    )

    return report, eval_df