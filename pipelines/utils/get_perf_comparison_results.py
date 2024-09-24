from pipelines.openai_langchain import openai_langchain_pipeline
from pipelines.mistral_llamaindex import mistralai_llamaindex_pipeline
from pipelines.performance_evaluation import langsmith_evaluation_pipeline


def get_performance_comparison_results(st):
    if not st.session_state.comparison_results:
        # Run the evaluation
        openai_evaluation_results = langsmith_evaluation_pipeline(
            openai_langchain_pipeline
        )
        mistralai_evaluation_results = langsmith_evaluation_pipeline(
            mistralai_llamaindex_pipeline
        )

        comparison_results = {}

        comparison_results["Openai"] = openai_evaluation_results
        comparison_results["Mistralai"] = mistralai_evaluation_results

        st.session_state.comparison_results = comparison_results
