from langgraph.graph import StateGraph,START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated,Sequence
from langchain_core.messages import BaseMessage
import os
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_info: str
    query: str

class agent_main:
    def __init__(self,controller):
        self.controller = controller
        self.tool_list=os.environ.get("TOOL_LIST",[])
        self.app=None
        self.init_graph()
    def init_graph(self,):
        self.init_tools()
        self.app = self.graph_builder()
        
    def init_tools(self):
        if "rag" in self.tool_list:
            # self.tool_list.append(self.tools.default_rag)
            pass
        if "product_rag" in self.tool_list:
            # self.tool_list.append(self.tools.product_rag)
            pass
        # self.controller.lang_utils.binding_tools(self.tool_list)
        
    def graph_builder(self):
        graph = StateGraph(State)
        graph.add_edge(START,"reasoner")
        graph.add_node("reasoner",self.controller.call_llm)
        if len(self.tool_list)>0:
            graph.add_node("tools", ToolNode(self.tool_list))
            graph.add_conditional_edges(
                "reasoner",
                tools_condition
                )
            graph.add_edge("tools", "reasoner")
        memory = MemorySaver()
        graph_build = graph.compile(checkpointer=memory)
        # print(graph_build.get_graph().draw_mermaid())
        return graph_build
