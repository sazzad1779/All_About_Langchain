# ## import model loader library and init model
# from langchain.chat_models import init_chat_model
# model = init_chat_model(model="gpt-4o-mini", model_provider="openai",)

## import prompt library
from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+3", "output": "5"},
]

system = "you are helpful assistant. you will help to learn {subject} and note down i dont have prior knowledge."
chat_prompt = ChatPromptTemplate(
    [
        ("human","{input}"),
        ("ai","{output}"),
    ]   
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    # This is a prompt template used to format each individual example.
    example_prompt=chat_prompt,
)

print(few_shot_prompt)