## Setup the environment
#export OPENAI_API_KEY="your_openai_api_key"

## import model loader library
from langchain.chat_models import init_chat_model
model = init_chat_model(model="gpt-4o-mini", model_provider="openai",)
result = model.invoke("what is atom tell me in one line.")
print(result.content)
