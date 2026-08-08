# 6. Feature Selection

## 6.1 Introduction

Feature selection is the process of identifying the most informative variables for model training while removing redundant or less useful features.

In healthcare datasets, reducing unnecessary features improves model interpretability, minimizes overfitting, and simplifies deployment.

---

# 6.2 Objectives

The objectives of feature selection were:

- Improve predictive performance.
- Reduce model complexity.
- Eliminate redundant variables.
- Improve computational efficiency.
- Enhance model interpretability.

---

# 6.3 Selection Strategy

Feature selection was performed after data preprocessing and feature engineering.

The process involved:

- Reviewing feature relevance.
- Removing redundant attributes.
- Preserving clinically meaningful variables.
- Evaluating feature importance during model development.

The final feature set was selected based on both predictive performance and domain relevance.

---

# 6.4 Clinical Relevance

Healthcare datasets often contain variables that are statistically useful but clinically difficult to interpret.

Priority was therefore given to variables that were:

- Clinically meaningful.
- Available before patient discharge.
- Relevant for predicting 30-day readmission.

This ensured that the final model remained practical for real-world clinical use.

---

# 6.5 Final Feature Categories

The selected features represent multiple aspects of a patient's hospital encounter.

Major categories include:

- Demographic Features
- Admission Information
- Clinical Indicators
- Laboratory Measurements
- Hospital Utilization
- Comorbidity Information
- Financial Variables

This combination provides a balanced representation of patient health and hospitalization characteristics.

---

# 6.6 Benefits

Feature selection provided several advantages:

- Reduced dimensionality.
- Faster model training.
- Lower computational cost.
- Improved generalization.
- Better interpretability.

It also simplified the deployment pipeline by reducing the number of required input variables.

---

# 6.7 Summary

Feature selection ensured that the predictive model was trained using informative and clinically relevant variables while avoiding unnecessary complexity.

The resulting feature set formed the foundation for model development discussed in the next chapter.
