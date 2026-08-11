import json
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BASE_DIR / "schema" / "validation_schema.json"


def load_schema(schema_path=SCHEMA_PATH):
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_blank(series):
    return series.isna() | (series.astype(str).str.strip() == "")


def validate_batch(df, schema):
    errors = []
    warnings = []

    df = df.copy()

    # Remove system-generated columns if accidentally uploaded
    ignore_cols = schema.get("ignore_if_uploaded", [])
    for col in ignore_cols:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
            warnings.append(f"Removed system-generated column: {col}")

    columns_schema = schema.get("columns", {})
    required_columns = schema.get("required_columns", [])

    # Check missing required columns
    missing_required = [c for c in required_columns if c not in df.columns]
    if missing_required:
        errors.append(f"Missing required columns: {missing_required}")

    # Warn unknown columns
    known_columns = set(columns_schema.keys())
    unknown_columns = [c for c in df.columns if c not in known_columns]
    if unknown_columns:
        warnings.append(f"Unknown columns ignored: {unknown_columns}")

    parsed_dates = {}

    # Column-wise validation
    for col, rules in columns_schema.items():
        if col not in df.columns:
            continue

        series = df[col]

        if series.dtype == object:
            series = series.astype(str).str.strip()

        blank_mask = is_blank(series)
        non_blank_mask = ~blank_mask

        # Required check
        if rules.get("required", False) and blank_mask.any():
            errors.append(f"Required column '{col}' has {blank_mask.sum()} blank values.")

        if non_blank_mask.sum() == 0:
            continue

        data_type = rules.get("data_type")
        allowed_values = rules.get("allowed_values")

        # Date validation
        if data_type == "date":
            parsed = pd.to_datetime(
                series[non_blank_mask],
                format="%d-%m-%Y",
                errors="coerce"
            )

            invalid_count = parsed.isna().sum()

            if invalid_count > 0:
                errors.append(
                    f"Column '{col}' has {invalid_count} invalid date values. Expected DD-MM-YYYY."
                )

            parsed_dates[col] = parsed

        # Numeric validation
        elif data_type in ["integer", "float"]:
            numeric = pd.to_numeric(series[non_blank_mask], errors="coerce")

            invalid_count = numeric.isna().sum()
            if invalid_count > 0:
                errors.append(
                    f"Column '{col}' has {invalid_count} non-numeric values."
                )

            min_value = rules.get("min")
            max_value = rules.get("max")

            valid_numeric = numeric.dropna()

            if min_value is not None and (valid_numeric < min_value).any():
                bad_count = (valid_numeric < min_value).sum()
                errors.append(
                    f"Column '{col}' has {bad_count} values below minimum {min_value}."
                )

            if max_value is not None and (valid_numeric > max_value).any():
                bad_count = (valid_numeric > max_value).sum()
                errors.append(
                    f"Column '{col}' has {bad_count} values above maximum {max_value}."
                )

                # Binary validation: 0 or 1
        elif data_type == "binary":
            raw = series[non_blank_mask]
            numeric = pd.to_numeric(raw, errors="coerce")

            # Check numeric values like 1.0, 0.0
            numeric_mask = numeric.notna()
            invalid_numeric = numeric_mask & ~numeric.isin([0, 1])

            if invalid_numeric.any():
                errors.append(
                    f"Binary column '{col}' has {invalid_numeric.sum()} invalid numeric values. Allowed: 0, 1."
                )

            # Check non-numeric string values
            string_mask = ~numeric_mask
            if string_mask.any():
                string_values = raw[string_mask].astype(str).str.strip().str.upper()
                invalid_string = ~string_values.isin({"0", "1"})

                if invalid_string.any():
                    errors.append(
                        f"Binary column '{col}' has {invalid_string.sum()} invalid string values. Allowed: 0, 1."
                    )

        # Boolean validation: TRUE/FALSE
        elif data_type == "boolean":
            values = series[non_blank_mask].astype(str).str.upper()

            valid_values = {"TRUE", "FALSE"}
            invalid_count = (~values.isin(valid_values)).sum()

            if invalid_count > 0:
                errors.append(
                    f"Boolean column '{col}' has {invalid_count} invalid values. Allowed: TRUE, FALSE."
                )

        # Categorical validation
        elif data_type == "categorical":
            if allowed_values:
                values = series[non_blank_mask].astype(str)
                allowed_strings = [str(v) for v in allowed_values]

                invalid_count = (~values.isin(allowed_strings)).sum()

                if invalid_count > 0:
                    if "Others" in allowed_strings:
                        warnings.append(
                            f"Categorical column '{col}' has {invalid_count} values not in allowed list. "
                            f"They will be mapped to Others during cleaning."
                        )
                    else:
                        errors.append(
                            f"Categorical column '{col}' has {invalid_count} invalid values. "
                            f"Allowed: {allowed_strings}"
                        )

    # Cross-check: admit_date <= discharge_date
    if "admit_date" in parsed_dates and "discharge_date" in parsed_dates:
        admit = parsed_dates["admit_date"]
        discharge = parsed_dates["discharge_date"]

        common_index = admit.index.intersection(discharge.index)

        if len(common_index) > 0:
            invalid_dates = (admit[common_index] > discharge[common_index]).sum()

            if invalid_dates > 0:
                errors.append(
                    f"{invalid_dates} rows have admit_date greater than discharge_date."
                )

    report = {
        "status": "passed" if len(errors) == 0 else "failed",
        "row_count": len(df),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors[:50],
        "warnings": warnings[:50]
    }

    return report