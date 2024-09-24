from langsmith import Client
from langsmith.evaluation import evaluate
import uuid
from pipelines.utils.performance_evaluators import (
    answer_accuracy_evaluator,
    answer_helpfulness_evaluator,
    answer_hallucination_evaluator,
)
from pipelines.utils.extract_scores import extract_scores
from pipelines.utils.perf_evals_dataset import inputs, outputs


def langsmith_evaluation_pipeline(rag_pipeline):
    results = {}

    # Create dataset & examples data in Langchain client db
    client = Client()
    uid = str(uuid.uuid4())

    dataset_name = f"RAG_pipelines_evaluation_dataset - {uid}"
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Questions and ground truth answers pairs about ANZ motor insurance",
    )

    client.create_examples(
        inputs=[{"question": q} for q in inputs],
        outputs=[{"answer": a} for a in outputs],
        dataset_id=dataset.id,
    )

    def predict_rag_answer(example: dict):
        response = rag_pipeline(example["question"])
        return {"answer": response["answer"]}

    def predict_rag_answer_with_context(example: dict):
        response = rag_pipeline(example["question"])
        return {"answer": response["answer"], "contexts": response["contexts"]}

    # TODO: error handling
    answer_experiment_results = evaluate(
        predict_rag_answer,
        data=dataset_name,
        evaluators=[answer_helpfulness_evaluator, answer_accuracy_evaluator],
        experiment_prefix="rag-answer-evaluations",
        metadata={
            "variant": "pdfs context, gpt-3.5-turbo",
            "version": "1.0.0",
            "revision_id": "beta",
        },
    )

    context_experiment_results = evaluate(
        predict_rag_answer_with_context,
        data=dataset_name,
        evaluators=[answer_hallucination_evaluator],
        experiment_prefix="rag-answer-hallucination-evaluations",
        metadata={
            "variant": "pdfs context, gpt-3.5-turbo",
            "version": "1.0.0",
            "revision_id": "beta",
        },
    )

    extract_scores(answer_experiment_results, finalResults=results)
    extract_scores(context_experiment_results, finalResults=results)

    return results
