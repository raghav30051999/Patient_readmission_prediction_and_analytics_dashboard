import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BASE_DIR / "schema" / "validation_schema.json"


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def replace_blank_with_nan(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(
                {
                    "": np.nan,
                    "nan": np.nan,
                    "NaN": np.nan,
                    "None": np.nan,
                    "null": np.nan
                }
            )
    return df


def clean_dates(df, report):
    date_columns = ["admit_date", "discharge_date"]

    for col in date_columns:
        if col in df.columns:
            parsed = pd.to_datetime(
                df[col],
                format="%d-%m-%Y",
                errors="coerce"
            )

            valid_count = parsed.notna().sum()
            df[col] = parsed

            report["changes"].append(
                f"{col}: parsed {valid_count} valid dates"
            )

    return df


def fill_los_days(df, report):
    required_cols = ["admit_date", "discharge_date", "los_days"]

    if all(col in df.columns for col in required_cols):
        df["los_days"] = pd.to_numeric(df["los_days"], errors="coerce")

        date_diff = (df["discharge_date"] - df["admit_date"]).dt.days

        fill_mask = (
            df["los_days"].isna() &
            date_diff.notna() &
            (date_diff >= 0)
        )

        if fill_mask.any():
            df.loc[fill_mask, "los_days"] = date_diff[fill_mask]

            report["changes"].append(
                f"los_days: filled {fill_mask.sum()} missing values using date difference"
            )

    return df


def clean_numeric(df, schema, report):
    columns_schema = schema.get("columns", {})

    for col, rules in columns_schema.items():
        if col not in df.columns:
            continue

        if rules.get("data_type") not in ["integer", "float"]:
            continue

        before = df[col].copy()

        df[col] = pd.to_numeric(df[col], errors="coerce")

        converted_to_blank = (before.notna() & df[col].isna()).sum()

        if converted_to_blank > 0:
            report["warnings"].append(
                f"{col}: {converted_to_blank} non-numeric values converted to blank"
            )

        min_value = rules.get("min")
        max_value = rules.get("max")

        if min_value is not None or max_value is not None:
            out_of_range = df[col].notna()

            if min_value is not None:
                out_of_range = out_of_range & (df[col] < min_value)

            if max_value is not None:
                out_of_range = out_of_range | (
                    df[col].notna() & (df[col] > max_value)
                )

            if out_of_range.any():
                report["warnings"].append(
                    f"{col}: {out_of_range.sum()} values outside expected range"
                )

    return df


def fill_costs(df, report):
    cost_cols = ["total_cost_inr", "govt_subsidy_inr", "out_of_pocket_inr"]

    if all(col in df.columns for col in cost_cols):

        # Fill total_cost_inr if missing
        total_missing = (
            df["total_cost_inr"].isna() &
            df["govt_subsidy_inr"].notna() &
            df["out_of_pocket_inr"].notna()
        )

        if total_missing.any():
            df.loc[total_missing, "total_cost_inr"] = (
                df.loc[total_missing, "govt_subsidy_inr"] +
                df.loc[total_missing, "out_of_pocket_inr"]
            )

            report["changes"].append(
                f"total_cost_inr: filled {total_missing.sum()} values using subsidy + out_of_pocket"
            )

        # Fill govt_subsidy_inr if missing
        govt_missing = (
            df["govt_subsidy_inr"].isna() &
            df["total_cost_inr"].notna() &
            df["out_of_pocket_inr"].notna()
        )

        if govt_missing.any():
            derived_govt = (
                df.loc[govt_missing, "total_cost_inr"] -
                df.loc[govt_missing, "out_of_pocket_inr"]
            )

            valid = derived_govt >= 0

            if valid.any():
                df.loc[derived_govt[valid].index, "govt_subsidy_inr"] = derived_govt[valid]

                report["changes"].append(
                    f"govt_subsidy_inr: filled {valid.sum()} values using total_cost - out_of_pocket"
                )

        # Fill out_of_pocket_inr if missing
        oop_missing = (
            df["out_of_pocket_inr"].isna() &
            df["total_cost_inr"].notna() &
            df["govt_subsidy_inr"].notna()
        )

        if oop_missing.any():
            derived_oop = (
                df.loc[oop_missing, "total_cost_inr"] -
                df.loc[oop_missing, "govt_subsidy_inr"]
            )

            valid = derived_oop >= 0

            if valid.any():
                df.loc[derived_oop[valid].index, "out_of_pocket_inr"] = derived_oop[valid]

                report["changes"].append(
                    f"out_of_pocket_inr: filled {valid.sum()} values using total_cost - govt_subsidy"
                )

    return df


def clean_binary(df, schema, report):
    columns_schema = schema.get("columns", {})

    for col, rules in columns_schema.items():
        if col not in df.columns:
            continue

        if rules.get("data_type") != "binary":
            continue

        raw = df[col]

        if raw.dtype == object:
            raw = raw.astype(str).str.upper().str.strip()
            raw = raw.replace(
                {
                    "": np.nan,
                    "NAN": np.nan,
                    "NONE": np.nan,
                    "NULL": np.nan,
                    "TRUE": "1",
                    "FALSE": "0"
                }
            )

        numeric = pd.to_numeric(raw, errors="coerce")

        if col == "readmitted_30d":
            invalid = numeric.notna() & ~numeric.isin([0, 1])

            if invalid.any():
                report["warnings"].append(
                    f"readmitted_30d: {invalid.sum()} invalid values converted to blank"
                )

                numeric[invalid] = np.nan

            df[col] = numeric

        else:
            before_blank = numeric.isna().sum()

            invalid = numeric.notna() & ~numeric.isin([0, 1])

            if invalid.any():
                report["warnings"].append(
                    f"{col}: {invalid.sum()} invalid binary values treated as 0"
                )

                numeric[invalid] = 0

            df[col] = numeric.fillna(0).astype(int)

            if before_blank > 0:
                report["changes"].append(
                    f"{col}: filled {before_blank} missing values with 0"
                )

    return df


def clean_boolean(df, schema, report):
    columns_schema = schema.get("columns", {})

    fill_defaults = {
        "bpl_card": 0,
        "teaching": 0
    }

    for col, rules in columns_schema.items():
        if col not in df.columns:
            continue

        if rules.get("data_type") != "boolean":
            continue

        before_blank = df[col].isna().sum()

        values = df[col].astype(str).str.upper().str.strip()

        values = values.replace(
            {
                "": np.nan,
                "NAN": np.nan,
                "NONE": np.nan,
                "NULL": np.nan
            }
        )

        values = values.map(
            {
                "TRUE": 1,
                "FALSE": 0,
                "1": 1,
                "0": 0
            }
        )

        values = pd.to_numeric(values, errors="coerce")

        if col in fill_defaults:
            filled_count = values.isna().sum()
            values = values.fillna(fill_defaults[col])

            if filled_count > 0:
                report["changes"].append(
                    f"{col}: filled {filled_count} missing values with {fill_defaults[col]}"
                )

        df[col] = values.astype(int)

    return df


def clean_categorical(df, schema, report):
    columns_schema = schema.get("columns", {})

    for col, rules in columns_schema.items():
        if col not in df.columns:
            continue

        if rules.get("data_type") != "categorical":
            continue

        allowed_values = rules.get("allowed_values")

        if not allowed_values:
            continue

        allowed_strings = [str(value) for value in allowed_values]

        values = df[col].astype(str).str.strip()

        values = values.replace(
            {
                "": np.nan,
                "nan": np.nan,
                "NaN": np.nan,
                "None": np.nan,
                "null": np.nan
            }
        )

        if "Others" in allowed_strings:
            missing_count = values.isna().sum()

            if missing_count > 0:
                report["changes"].append(
                    f"{col}: filled {missing_count} missing values with Others"
                )

            values = values.fillna("Others")

            invalid_mask = ~values.isin(allowed_strings)

            if invalid_mask.any():
                report["changes"].append(
                    f"{col}: mapped {invalid_mask.sum()} invalid values to Others"
                )

                values[invalid_mask] = "Others"

        else:
            invalid_mask = values.notna() & ~values.isin(allowed_strings)

            if invalid_mask.any():
                report["warnings"].append(
                    f"{col}: {invalid_mask.sum()} values not in allowed list"
                )

        df[col] = values

    return df


def clean_batch(df, schema=None):
    if schema is None:
        schema = load_schema()

    cleaned = df.copy()

    report = {
        "rows_input": len(cleaned),
        "rows_output": len(cleaned),
        "changes": [],
        "warnings": []
    }

    # Remove system-generated prediction columns if uploaded
    ignore_cols = schema.get("ignore_if_uploaded", [])
    for col in ignore_cols:
        if col in cleaned.columns:
            cleaned.drop(columns=[col], inplace=True)
            report["warnings"].append(
                f"Removed system-generated column: {col}"
            )

    cleaned = replace_blank_with_nan(cleaned)
    cleaned = clean_dates(cleaned, report)
    cleaned = fill_los_days(cleaned, report)
    cleaned = clean_numeric(cleaned, schema, report)
    cleaned = fill_costs(cleaned, report)
    cleaned = clean_binary(cleaned, schema, report)
    cleaned = clean_boolean(cleaned, schema, report)
    cleaned = clean_categorical(cleaned, schema, report)

    report["rows_output"] = len(cleaned)

    return cleaned, report