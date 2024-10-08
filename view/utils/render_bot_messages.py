def render_chatbot_messages(st):

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])

            if message["role"] == "assistant":

                col1, col2 = st.columns([5, 5])

                with col1:
                    if message["content"]["summary"]:
                        file_index = message["content"]["file_index"]
                        if file_index == 0:
                            st.subheader(f"OpenAI and Langchain pipeline")
                        st.divider()
                        uploaded_file_name = message["content"]["uploaded_file_name"]
                        st.markdown(f"**Summary of {uploaded_file_name}**")
                    st.markdown(
                        message["content"]["openai_response"].replace("$", "\$")
                    )

                with col2:
                    if message["content"]["summary"]:
                        file_index = message["content"]["file_index"]
                        if file_index == 0:
                            st.subheader(f"MistralAI and LlamaIndex pipeline")
                        st.divider()
                        uploaded_file_name = message["content"]["uploaded_file_name"]
                        st.markdown(f"**Summary of {uploaded_file_name}**")
                    st.markdown(
                        message["content"]["mistralai_response"].replace("$", "\$")
                    )
