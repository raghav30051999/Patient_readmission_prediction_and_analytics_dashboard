def generate_recommendations(patient):

    recommendations = []

    # =====================================================
    # Risk-based Recommendations
    # =====================================================

    if patient["Probability"] >= 0.60:

        recommendations.append(
            ("high", "Arrange follow-up within 7 days.")
        )

        recommendations.append(
            ("high", "Perform a comprehensive medication review.")
        )

        recommendations.append(
            ("high", "Coordinate with the primary care physician.")
        )

    elif patient["Probability"] >= 0.30:

        recommendations.append(
            ("moderate", "Schedule follow-up within 14 days.")
        )

        recommendations.append(
            ("moderate", "Reinforce discharge instructions.")
        )

    else:

        recommendations.append(
            ("low", "Continue routine follow-up as per hospital protocol.")
        )

    # =====================================================
    # Clinical Recommendations
    # =====================================================

    if patient["prev_admissions"] >= 2:

        recommendations.append(
            ("info", "Previous readmissions detected. Assign a care coordinator.")
        )

    if patient["hba1c"] >= 7:

        recommendations.append(
            ("info", "Optimize diabetes management and monitor HbA1c.")
        )

    if patient["creatinine"] >= 1.5:

        recommendations.append(
            ("info", "Monitor renal function and consider nephrology consultation.")
        )

    if patient["haemoglobin"] < 11:

        recommendations.append(
            ("info", "Evaluate and manage anemia.")
        )

    if patient["los_days"] >= 10:

        recommendations.append(
            ("info", "Early outpatient review due to prolonged hospital stay.")
        )

    if patient["age"] >= 65:

        recommendations.append(
            ("info", "Ensure caregiver support and assess fall risk.")
        )

    if patient["charlson_index"] >= 5:

        recommendations.append(
            ("info", "Multiple chronic illnesses detected. Consider multidisciplinary follow-up.")
        )

    return recommendations