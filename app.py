from rag_pipelines.openai_langchain import openai_langchain_pipeline
from rag_pipelines.mistral_llamaindex import mistralai_llamaindex_pipeline

def main():
   query = 'What is the cooling off period for an allianz personal motor insurance?'
   openai_answer = openai_langchain_pipeline(query)
   mistralai_answer = mistralai_llamaindex_pipeline(query)
   print(f"openai_answer: {openai_answer}")
   print(f"mistralai_answer: {mistralai_answer}")
   
    
if __name__ == "__main__":
    main()