from langchain_core.prompts import ChatPromptTemplate
from langchain_core.load import dump,dumpd,dumps,load,loads
prompt  = ChatPromptTemplate(
    [
        ("system","you are helpful assistant."),
        ("human","what is atom?")     
     ]
)
prompt.pretty_print()
string_representation = dumps(prompt, pretty=True)
print(string_representation)
print(prompt.lc_secrets)

# prompt.save("/.prompt.json")
# print(prompt.format_messages())