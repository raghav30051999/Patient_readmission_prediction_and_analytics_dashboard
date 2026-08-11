import pandas as pd
from agent_pipeline.data_cleaner import clean_batch
from agent_pipeline.predictor import predict_batch
from agent_pipeline.evaluator import evaluate_batch

def run_agent_pipeline(df):
    """
    Agentic Orchestrator: Automatically chains cleaning, prediction, and evaluation.
    """
    agent_report = {
        "status": "success",
        "stages_completed": [],
        "cleaning_report": None,
        "prediction_report": None,
        "evaluation_report": None,
        "messages": []
    }

    # Stage 1: Data Cleaning
    try:
        cleaned_df, cleaning_report = clean_batch(df)
        agent_report["cleaning_report"] = cleaning_report
        agent_report["stages_completed"].append("Data Cleaning")
    except Exception as e:
        agent_report["status"] = "failed"
        agent_report["messages"].append(f"Data Cleaning failed: {str(e)}")
        return df, agent_report

    # Stage 2: Prediction
    try:
        predicted_df, prediction_report = predict_batch(cleaned_df)
        agent_report["prediction_report"] = prediction_report
        agent_report["stages_completed"].append("Prediction")
    except Exception as e:
        agent_report["status"] = "failed"
        agent_report["messages"].append(f"Prediction failed: {str(e)}")
        return cleaned_df, agent_report

    # Stage 3: Evaluation (only runs if actual outcomes exist)
    try:
        evaluation_report, evaluation_df = evaluate_batch(predicted_df)
        agent_report["evaluation_report"] = evaluation_report
        agent_report["stages_completed"].append("Evaluation")
    except Exception as e:
        agent_report["status"] = "partial_success"
        agent_report["messages"].append(f"Evaluation failed: {str(e)}")
        return predicted_df, agent_report

    agent_report["messages"].append(
        f"Agent successfully completed {len(agent_report['stages_completed'])} stages autonomously."
    )

    return predicted_df, agent_report