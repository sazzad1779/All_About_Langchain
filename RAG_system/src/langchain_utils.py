from langchain.chat_models import init_chat_model
import os

class LangchainUtils:
    def __init__(self,controller):
        self.controller = controller
        self.init_chat_model()
        self.init_embed_model()
        
    def init_chat_model(self):
        self.controller.chat_model = init_chat_model(model=os.environ.get("MODEL_NAME"),model_provider=os.environ.get("MODEL_PROVIDER"))
        
    def init_embed_model(self):
        from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
        self.controller.embed_model = GoogleGenerativeAIEmbeddings(model=os.environ.get("EMBED_MODEL_NAME"))
    
    def call_llm(self,query):     
        response = self.controller.rag_chain.invoke(query)
        return response