from langchain import hub
from langchain_openai import ChatOpenAI

# Grade prompt
grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")
grade_prompt_answer_helpfulness = prompt = hub.pull(
    "langchain-ai/rag-answer-helpfulness"
)
grade_prompt_hallucinations = prompt = hub.pull("langchain-ai/rag-answer-hallucination")


def answer_accuracy_evaluator(run, example) -> dict:

    # Get question, ground truth answer, RAG chain answer
    input_question = example.inputs["question"]
    reference = example.outputs["answer"]
    prediction = run.outputs["answer"]

    # LLM grader
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Structured prompt
    answer_grader = grade_prompt_answer_accuracy | llm

    # Run evaluator
    score = answer_grader.invoke(
        {
            "question": input_question,
            "correct_answer": reference,
            "student_answer": prediction,
        }
    )

    score = score["Score"]

    return {"key": "answer_accuracy_score", "score": score}


def answer_helpfulness_evaluator(run, example) -> dict:
    # Get question, ground truth answer, RAG chain answer
    input_question = example.inputs["question"]
    prediction = run.outputs["answer"]

    # LLM grader
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Structured prompt
    answer_grader = grade_prompt_answer_helpfulness | llm

    # Run evaluator
    score = answer_grader.invoke(
        {"question": input_question, "student_answer": prediction}
    )
    score = score["Score"]

    return {"key": "answer_helpfulness_score", "score": score}


def answer_hallucination_evaluator(run, example) -> dict:
    # RAG inputs
    contexts = run.outputs["contexts"]

    # RAG answer
    prediction = run.outputs["answer"]

    # LLM grader
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # Structured prompt
    answer_grader = grade_prompt_hallucinations | llm

    # Get score
    score = answer_grader.invoke(
        {
            "documents": contexts,
            "student_answer": prediction,
        }
    )
    score = score["Score"]

    return {"key": "answer_hallucination_score", "score": score}
