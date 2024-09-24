PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}

Answer the question based on the above context: {question}.

Provide a detailed answer.
Don't justify your answers.
Don't give information not mentioned in the CONTEXT INFORMATION.
Do not say "according to the context" or "mentioned in the context" or similar.

If you cannot find an answer ask the user to rephrase the question.
answer:
"""
