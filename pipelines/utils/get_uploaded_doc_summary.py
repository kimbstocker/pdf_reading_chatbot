import os
from pipelines.openai_langchain import openai_langchain_pipeline
from pipelines.mistral_llamaindex import mistralai_llamaindex_pipeline

def get_uploaded_doc_summary(st, uploaded_files):
    
   if not st.session_state.chat_actions_triggered:
      # upload/write file in the data folder
      for index, uploaded_file in enumerate(uploaded_files):
         uploaded_file_name = uploaded_file.name
            
         if uploaded_file_name not in st.session_state.uploaded_file_names:
            
            with open(os.path.join(os.environ['DATASET_PATH'], uploaded_file_name), "wb") as f:
               f.write(uploaded_file.getbuffer())
               
            query = "Summarise this document, make it concise and relevant to the provided context. Your answer should not be longer than 250 words"
               
            openai_docs_summary = openai_langchain_pipeline(query, uploaded_file_name)
            mistralai_docs_summary = mistralai_llamaindex_pipeline(query, uploaded_file_name)
            
            st.session_state.messages.append(
               {
                  "role": "assistant",
                  "content": 
                     {  
                        "openai_response": openai_docs_summary["answer"],
                        "mistralai_response": mistralai_docs_summary["answer"],
                        "summary": True,
                        "uploaded_file_name": uploaded_file_name,
                        "file_index": index
                     } 
               }
            )
            
            st.session_state.uploaded_file_names.append(uploaded_file_name)