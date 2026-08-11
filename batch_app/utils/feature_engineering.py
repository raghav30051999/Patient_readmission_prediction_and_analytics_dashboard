import numpy as np

def create_engineered_features(df):

    df = df.copy()

    # --------------------------------------------------
    # Phase 1
    # --------------------------------------------------

    df["procedures_per_day"] = (
        df["num_procedures"] /
        np.where(df["los_days"] == 0, 1, df["los_days"])
    )

    df["cost_per_day"] = (
        df["total_cost_inr"] /
        np.where(df["los_days"] == 0, 1, df["los_days"])
    )

    # --------------------------------------------------
    # Phase 2
    # --------------------------------------------------

    total = (
        df["govt_subsidy_inr"] +
        df["out_of_pocket_inr"]
    )

    df["subsidy_ratio"] = np.where(
        total == 0,
        0,
        df["govt_subsidy_inr"] / total
    )

    df["oop_ratio"] = np.where(
        total == 0,
        0,
        df["out_of_pocket_inr"] / total
    )

    # --------------------------------------------------
    # Phase 3
    # --------------------------------------------------

    df["severity_score"] = (
        df["charlson_index"] *
        df["comorbidity_count"]
    )

    df["age_severity"] = (
        df["age"] *
        df["charlson_index"]
    )

    df["charlson_density"] = (
        df["charlson_index"] /
        np.where(df["comorbidity_count"] == 0, 1, df["comorbidity_count"])
    )

    return df