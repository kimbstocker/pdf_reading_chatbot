import pandas as pd
from pipelines.utils.perf_evals_dataset import inputs


def createTableDataframe(data): 

    # Flatten the data into a list of dictionaries
    questions = inputs
    
    openai_hallucination = [list(item.values())[0] for item in data["Openai"]["answer_hallucination_score"]]
    openai_helpfulness = [list(item.values())[0] for item in data["Openai"]["answer_helpfulness_score"]]
    openai_accuracy = [list(item.values())[0] for item in data["Openai"]["answer_accuracy_score"]]

    # Extract scores for Mistralai
    mistralai_hallucination = [list(item.values())[0] for item in data["Mistralai"]["answer_hallucination_score"]]
    mistralai_helpfulness = [list(item.values())[0] for item in data["Mistralai"]["answer_helpfulness_score"]]
    mistralai_accuracy = [list(item.values())[0] for item in data["Mistralai"]["answer_accuracy_score"]]
    
    # Create a DataFrame for the table
    df = pd.DataFrame({
        "Question": questions,
        "OpenAI Hallucination Score": openai_hallucination,
        "OpenAI Helpfulness Score": openai_helpfulness,
        "OpenAI Accuracy Score": openai_accuracy,
        "Mistralai Hallucination Score": mistralai_hallucination,
        "Mistralai Helpfulness Score": mistralai_helpfulness,
        "Mistralai Accuracy Score": mistralai_accuracy
    })

    return df
