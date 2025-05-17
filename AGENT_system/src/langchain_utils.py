from langchain.chat_models import init_chat_model
from langchain_core.messages import trim_messages
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
import os
from RAG_system.src.prompts import system_message

class LangchainUtils:
    def __init__(self,controller):
        self.controller = controller
        self.init_chat_model()
        self.init_embed_model()
        
        
    def init_chat_model(self):
        self.controller.chat_model = init_chat_model(model=os.environ.get("MODEL_NAME"),provider=os.environ.get("MODEL_PROVIDER"))
        
    def init_embed_model(self):
        from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
        self.controller.embed_model = GoogleGenerativeAIEmbeddings(model=os.environ.get("EMBED_MODEL_NAME"))
    
    def init_prompt_utils(self):
        self.controller.trimmer = trim_messages(
            max_tokens=4,#65,
            strategy = "last",
            # token_counter = count_tokens_approximately,#llm, it is taking time
            token_counter=len,
            include_system = True,
            allow_partial=False,
            start_on= "human",
            end_on=("human", "tool"),
            )
        self.controller.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system",system_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
     