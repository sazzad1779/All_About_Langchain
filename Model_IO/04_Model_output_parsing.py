## Setup the environment
#export OPENAI_API_KEY="your_openai_api_key"

# ## import model loader library and init model
from langchain.chat_models import init_chat_model
model = init_chat_model(model="gpt-4o-mini", model_provider="openai",)



from langchain.schema.output_parser import StrOutputParser
'''
Simply returns the string from the model.
Useful when you just want raw text.
'''
parser = StrOutputParser()
parser.invoke("hi")
print(parser.get_format_instructions)

result = parser.parse("Hello, how are you?")
print(result)  # Output: Hello, how are you?

from langchain.output_parsers import CommaSeparatedListOutputParser

'''
Turns a comma-separated string into a Python list.
'''

parser = CommaSeparatedListOutputParser()
output = parser.parse("apple, banana, cherry")
print(output)  # ['apple', 'banana', 'cherry']



