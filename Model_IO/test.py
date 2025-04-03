from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage
prompt = ChatPromptTemplate.from_messages([
    SystemMessage("You are a helpful assistant."),
    ("user", "Tell me a fun fact about {topic}.")
])
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What's the capital of {Japan}?")
]
formatted = prompt.format_messages(topic="spiders")
print(formatted)
print(messages)
for msg in formatted:
    print(f"[{msg.type}] {msg.content}")