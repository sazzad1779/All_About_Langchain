from langchain_core.messages import HumanMessage
class controller:
    def __init__(self):
        self.chat_model = None
        self.embed_model = None
        self.vectordb_type=None
        self.vectordb_retrieval = None
        self.prompt_template = None
        self.rag_chain = None
        

    
    def info(self,):
        print(f"Initialized llm: {self.chat_model}")
        print(f"Initialized embed model: {self.embed_model}")
        print(f"{self.vectordb_type} Vector db using.")
