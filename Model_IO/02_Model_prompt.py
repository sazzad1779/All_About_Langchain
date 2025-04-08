## Setup the environment
#export OPENAI_API_KEY="your_openai_api_key"

# ## import model loader library and init model
from langchain.chat_models import init_chat_model
model = init_chat_model(model="gpt-4o-mini", model_provider="openai",)

## import prompt library
from langchain_core.prompts import ChatPromptTemplate
system = "you are helpful assistant. you will help to learn {subject} and note down i dont have prior knowledge."
chat_prompt = ChatPromptTemplate(
    [
        ("system",system),
        ("human","{human}"),
    ]   
)
chain =chat_prompt | model 
# print(chain)
# print(chat_prompt,"\n")
result = chain.invoke({"subject":"ML","human":"tell me about overfitting."})
# print(result)

## Example 2
# human = " i need to know about how to optimize the inference of llm."
# chat_prompt = ChatPromptTemplate(
#     [
#         ("system"," you are helpful assistant. you will help to learn {subject} and note down i dont have prior knowledge."),
#         ("human","{human}"),
#     ]   
# )
# chat_prompt = chat_prompt.invoke(
#     {"subject":"Machine learning",
#      "human":" i need to know about how to optimize the inference of llm."
#      }
# )
# print(chat_prompt,"\n")
# result = model.invoke(chat_prompt)
# print(result)

## Example 3
# chat_prompt = ChatPromptTemplate(
#     [
#         ("system"," you are helpful assistant. you will help to learn ML and note down i dont have prior knowledge."),
#         ("human","{human}"),
#     ]   
# )
# chat_prompt = chat_prompt.invoke(" i need to know about how to optimize the inference of llm.")


# print(chat_prompt,"\n")
# result = model.invoke(chat_prompt)
# print(result)
