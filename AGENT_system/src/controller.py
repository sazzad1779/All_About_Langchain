from langchain_core.messages import HumanMessage
class controller:
    def __init__(self):
        self.chat_model = None
        self.embed_model = None
        self.vectordb_type=None
        self.vectordb_retrieval = None
        self.message_trimmer = None
        self.prompt_template = None
        
    def call_llm(self,state):
        trimmed_messages =self.message_trimmer.invoke(state["messages"])
        prompt = self.prompt_template.invoke(
            {"messages": trimmed_messages}
        )        
        response = self.chat_model.invoke(prompt)
        return {"messages":[response]}
    
    def call_agent(self,query:str,session_id):
        config = {"configurable": {"thread_id": session_id}}
        query = [HumanMessage(query)] 
        answer=self.app.invoke({"messages":query},config=config,)
        return answer['messages'][-1].content

    def info(self,):
        print(f"Initialized llm: {self.chat_model}")
        print(f"Initialized embed model: {self.embed_model}")
        print(f"{self.vectordb_type} Vector db using.")
