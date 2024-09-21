import os
from pipelines.openai_langchain import openai_langchain_pipeline
from pipelines.mistral_llamaindex import mistralai_llamaindex_pipeline
from pipelines.performance_evaluation import langsmith_evaluation_pipeline
import streamlit as st
from view.styles.st_custom_styles import custom_css
from view.utils.comparison_table import createTableDataframe

def main():
   
   st.set_page_config(page_title="PDF Reading AI Chatbot 🤖", layout="wide")

   st.title('PDF Reading AI Chatbot 🤖')

   st.markdown(custom_css, unsafe_allow_html=True)

   if "initialized" not in st.session_state:
      print("Initializing session state...")
      
      comparison_results = {}
      st.session_state.messages = []
      
      # Run the evaluation
      openai_evaluation_results = langsmith_evaluation_pipeline(openai_langchain_pipeline)
      mistralai_evaluation_results = langsmith_evaluation_pipeline(mistralai_llamaindex_pipeline)
         
      comparison_results["Openai"] = openai_evaluation_results
      comparison_results["Mistralai"] = mistralai_evaluation_results
            
      st.session_state.comparison_results = comparison_results 
      st.session_state.initialized = True   


   comparison_result = st.empty()
   
   if st.session_state.comparison_results: 
      with comparison_result.container():
         st.subheader(f"Performance comparison")
         st.markdown('The below comparison results are derived from using Langsmith')
         
         print(f"result--: {st.session_state.comparison_results}")  

         dataframe = createTableDataframe(st.session_state.comparison_results)
         st.table(dataframe)
          
   # handle upload files
   uploaded_files = st.file_uploader(
      "Choose one or more PDF file(s)",
      accept_multiple_files=True,
      type=['pdf']
   )
   
   # upload/write file in the data folder
   for uploaded_file in uploaded_files:
      with open(os.path.join(os.environ['DATASET_PATH'], uploaded_file.name), "wb") as f:
         f.write(uploaded_file.getbuffer())
   
   # render messages in session state
   for message in st.session_state.messages:
      with st.chat_message(message["role"]):
         if message["role"] == "user":
            st.markdown(message["content"])
                        
         if message["role"] == "assistant":
            col1, col2 = st.columns([5, 5])

            with col1: 
                  st.subheader(f"OpenAI and Langchain pipeline")
                  st.markdown(message["content"]["openai_response"]) 

            with col2: 
                  st.subheader(f"MistralAI and LlamaIndex pipline")
                  st.markdown(message["content"]["mistralai_response"]) 
   
   # define chat on_submit function to trigger streamlit app rerun and render nrew messages
   def chat_actions():
      prompt = st.session_state["prompt"]
      if not prompt:
         return
      
      st.session_state.messages.append({"role": "user", "content": prompt})
          
      openai_answer = openai_langchain_pipeline(prompt)["answer"]
      mistralai_answer = mistralai_llamaindex_pipeline(prompt)["answer"]

      print(f"openai_answer: {openai_answer}")
      print(f"mistralai_answer: {mistralai_answer}")
    
      st.session_state.messages.append(
         {
            "role": "assistant",
            "content": 
               {  
                  "openai_response": openai_answer,
                  "mistralai_response": mistralai_answer,
               } 
         }
      )
      
   st.chat_input("Ask me anything about the PDFs...", on_submit=chat_actions, key="prompt")

    
if __name__ == "__main__":
    main()