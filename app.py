import streamlit as st
from dotenv import load_dotenv
from pipelines.openai_langchain import openai_langchain_pipeline
from pipelines.mistral_llamaindex import mistralai_llamaindex_pipeline
from view.styles.st_custom_styles import custom_css
from view.utils.comparison_table import createTableDataframe
from view.utils.render_bot_messages import render_chatbot_messages
from pipelines.utils.get_uploaded_doc_summary import get_uploaded_doc_summary
from pipelines.utils.get_perf_comparison_results import (
    get_performance_comparison_results,
)


def main():
    load_dotenv()

    st.set_page_config(page_title="PDF Reading AI Chatbot 🤖", layout="wide")

    st.title("PDF Reading AI Chatbot 🤖")

    st.markdown(custom_css, unsafe_allow_html=True)

    if "initialized" not in st.session_state:
        print("Initializing session state...")

        st.session_state.messages = []
        st.session_state.chat_actions_triggered = False
        st.session_state.comparison_results = {}
        st.session_state.uploaded_file_names = []
        st.session_state.initialized = True

    comparison_result = st.empty()

    if st.session_state.comparison_results:
        with comparison_result.container():
            st.subheader(f"Performance comparison")
            st.markdown("The below comparison results are derived from using Langsmith")
            dataframe = createTableDataframe(st.session_state.comparison_results)
            st.table(dataframe)

    def generate_docs_summary():
        # reset below variables to generate new summary for the newly uploaded docs
        st.session_state.chat_actions_triggered = False

    # handle upload files
    uploaded_files = st.file_uploader(
        "Choose one or more PDF file(s)",
        accept_multiple_files=True,
        type=["pdf"],
        on_change=generate_docs_summary,
    )

    get_uploaded_doc_summary(st, uploaded_files)

    # render messages in session state
    render_chatbot_messages(st)

    # define chat on_submit function to trigger streamlit app rerun and render new messages
    def chat_actions():
        prompt = st.session_state["prompt"]
        if not prompt or len(st.session_state.uploaded_file_names) == 0:
            st.warning("Please upload a file before asking questions", icon="⚠️")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})

        openai_answer = openai_langchain_pipeline(prompt)["answer"]
        mistralai_answer = mistralai_llamaindex_pipeline(prompt)["answer"]

        print(f"openai_answer: {openai_answer}")
        print(f"mistralai_answer: {mistralai_answer}")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": {
                    "openai_response": openai_answer,
                    "mistralai_response": mistralai_answer,
                    "summary": False,
                },
            }
        )

        st.session_state.chat_actions_triggered = True

        # run evalutation performance tests and add results to session_state
        get_performance_comparison_results(st)

    st.chat_input(
        "Ask me anything about the PDFs...", on_submit=chat_actions, key="prompt"
    )


if __name__ == "__main__":
    main()
