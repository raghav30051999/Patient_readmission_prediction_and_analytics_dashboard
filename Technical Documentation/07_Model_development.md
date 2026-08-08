# 7. Model Development

## 7.1 Introduction

The objective of model development was to build a reliable machine learning model capable of predicting whether a patient would be readmitted within **30 days** after hospital discharge.

Several classification algorithms were evaluated before selecting the final production model.

---

# 7.2 Problem Formulation

The prediction task is formulated as a **binary classification problem**.

**Target Variable**

| Value | Meaning |
|------|---------|
| 0 | Not Readmitted |
| 1 | Readmitted within 30 Days |

The model predicts the probability that a patient belongs to the positive (readmitted) class.

---

# 7.3 Data Splitting

The dataset was divided into independent training and testing subsets before model development.

- Training Set : 80%
- Testing Set : 20%

A stratified train-test split was used to preserve the original class distribution in both datasets.

The **testing dataset remained completely unseen during model training and hyperparameter optimization** to provide an unbiased estimate of model performance.

---

# 7.4 Candidate Models

Multiple supervised learning algorithms were evaluated during experimentation.

The models considered included:

- Random Forest
- Balanced Random Forest
- XGBoost
- CatBoost

Each model was trained using the same training dataset and evaluated using identical performance metrics.

---

# 7.5 Why CatBoost?

CatBoost was selected as the final production model because it demonstrated the best balance between predictive performance and robustness.

Its advantages include:

- Better handling of categorical variables.
- Strong performance on tabular datasets.
- Reduced overfitting through ordered boosting.
- Minimal preprocessing requirements.
- High predictive accuracy.
- Stable probability estimates.

---

# 7.6 Threshold Optimization

The default classification threshold of **0.50** was not used.

Instead, multiple threshold values were evaluated to maximize the balance between precision and recall.

The final threshold (0.17-0.18) was selected using validation performance and optimized for healthcare decision support.

---

# 7.7 Evaluation Metrics

The models were evaluated using multiple metrics rather than relying solely on accuracy.

The primary evaluation metrics included:

- Precision
- Recall
- F1 Score
- ROC-AUC

Special emphasis was placed on Recall and F1 Score due to the healthcare nature of the problem.

Achieved ROC-AUC value of 0.76.

---

# 7.8 Model Persistence

After training, the final CatBoost model was serialized and stored using Joblib.

Persisting the trained model enables:

- Fast inference.
- Consistent predictions.
- Deployment without retraining.
- Easy integration into the Streamlit application.

---

# 7.9 Prediction Pipeline

The prediction workflow consists of the following stages:

1. Receive patient information.
2. Apply preprocessing.
3. Generate engineered features.
4. Pass the processed data to the trained CatBoost model.
5. Predict readmission probability.
6. Apply the optimized threshold.
7. Return the predicted class.
8. Display prediction results within the Streamlit interface.

---

# 7.10 Summary

Multiple machine learning algorithms were evaluated during experimentation.

CatBoost demonstrated the best overall performance and was selected as the production model due to its predictive capability, robustness, and suitability for structured healthcare data.

The next chapter presents the evaluation of the final model and discusses its predictive performance.