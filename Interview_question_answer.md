
## How do you create a simple chain in LangChain?

```python

## load llm
from langchain.chat_models import init_chat_model
model = init_chat_model(model="gpt-4o-mini", model_provider="openai",)

## create prompt
from langchain_core.prompts import ChatPromptTemplate
system = "you are helpful assistant. you will help to learn {subject} and note down i dont have prior knowledge."
chat_prompt = ChatPromptTemplate(
    [
        ("system",system),
        ("human","{human}"),
    ]   
)
```

``` python
# way 1
## simple chain
chain =prompt | model 
## invoke
result = chain.invoke({"subject":"ML","human":"tell me about overfitting."})
print(result)
```

``` python
#way 2 
##import memory
from langchain.memory import ConversationBufferMemory
memory= ConversationBufferMemory()

##conversational chain
from langchain.chains import ConversationChain
conv_chain = ConversationChain(llm=model,prompt=chat_prompt,memory=memory)

##invoke
result = chain({"subject":"ML","human":"tell me about overfitting."})
print(result)
```


## How do you add memory to a chain in LangChain?

``` python
##import memory
from langchain.memory import ConversationBufferMemory
memory= ConversationBufferMemory()

##conversational chain
from langchain.chains import ConversationChain
conv_chain = ConversationChain(llm=model,prompt=chat_prompt,memory=memory)

##invoke
result = chain({"subject":"ML","human":"tell me about overfitting."})
print(result)
```

## How do you create a custom tool for an agent in LangChain?

``` python
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```


## how to add output parser 
```python 
from langchain_core.output_parsers import StrOutputParser
parser= StrOutputParser()
chain = chat_prompt | model | parser
```