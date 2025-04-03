# Model Input ouput
## Model Loading
## Model Input Prompting

---

### 🤖 **PromptTemplate vs ChatPromptTemplate**

| Feature                    | `PromptTemplate`                     | `ChatPromptTemplate`                          |
|----------------------------|--------------------------------------|-----------------------------------------------|
| 📄 Format                  | Plain text prompt                    | Multi-turn chat (system, user, assistant)     |
| 🔧 Use Case                | Single-shot prompts                  | Conversational agents, chatbots               |
| 🧠 Used With               | `LLM` models (like `text-davinci-003`) | `ChatModel` (like `gpt-3.5`, `gpt-4`)         |
| 💬 Structure               | Just one message                     | Supports multiple roles: system, user, AI     |
| 📚 Prompt Blocks           | One block                            | Multiple messages as a list                   |

---

#### 🧪 Example 1: **PromptTemplate (Text Models)**

```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "What is the capital of {country}?"
)

final_prompt = prompt.format(country="Germany")
print(final_prompt)
# Output: What is the capital of Germany?
```

This is useful for **older text completion models** like `text-davinci-003`.

---

#### 💬 Example 2: **ChatPromptTemplate (Chat Models)**

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "What is the capital of {country}?")
])

final_prompt = prompt.format_messages(country="Germany")
for msg in final_prompt:
    print(msg)
    
# Output:
SystemMessage(content="You are a helpful assistant.")
HumanMessage(content="What is the capital of Germany?")
```

This is designed for **chat-based models** like `gpt-3.5-turbo` and `gpt-4`, which expect a list of messages, not just one big string.

---

#### 🔍 TL;DR:

| If you're using...      | Use...               | Why?                                     |
|-------------------------|----------------------|------------------------------------------|
| 🧠 Text models          | `PromptTemplate`     | They take plain strings as input         |
| 💬 Chat models (GPT-4) | `ChatPromptTemplate` | They expect a list of messages with roles|

---

#### Bonus Tip: Under the hood

`ChatPromptTemplate` builds a **list of `Messages`** (`SystemMessage`, `HumanMessage`, `AIMessage`)  
Whereas `PromptTemplate` builds a **plain string prompt**.

---


You're asking all the right questions—this one’s 🔑 for mastering **LangChain with chat models like GPT-3.5 or GPT-4**.

---



### 💬 What are Messages in `ChatPromptTemplate`?

In `ChatPromptTemplate`, you **build a conversation using a sequence of messages**. Each message has a **role** and **content**, which mimics how chat models work.



#### 👥 Types of Messages

| Role         | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `"system"`   | Sets the behavior, personality, or context for the AI.                      |
| `"user"`     | Represents the human/user input.                                            |
| `"assistant"`| Optional. Can include previous AI responses (useful in few-shot examples).  |

---

#### 🛠️ Example 1: Basic Usage of Messages

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Tell me a fun fact about {topic}.")
])

formatted = prompt.format_messages(topic="spiders")

for msg in formatted:
    print(f"[{msg.type}] {msg.content}")
```

**Output:**
```
[system] You are a helpful assistant.
[human] Tell me a fun fact about spiders.
```

Then you can pass this to `ChatOpenAI()`.

---

#### 🧠 How to Add Dynamic User Input

Use curly braces `{}` in the content of any message, and fill it in with `.format_messages()` or `.partial()`.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math tutor."),
    ("user", "Help me solve: {equation}")
])

msgs = prompt.format_messages(equation="5x + 3 = 18")
```

---

#### 💡 Example 2: Few-shot Example with Assistant + User Messages

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a coding assistant."),
    ("user", "Write a Python function to reverse a list."),
    ("assistant", "Sure! Here's a simple function:\n\ndef reverse_list(lst):\n    return lst[::-1]"),
    ("user", "Now write one to check if a string is a palindrome.")
])
```

This gives GPT a **demo** to learn from before handling the new request.

---

#### 💬 Example 3: Using Variables in Multiple Messages

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}."),
    ("user", "Explain the following concept in simple terms: {concept}")
])

msgs = prompt.format_messages(domain="quantum physics", concept="superposition")
```

This is super helpful to reuse one prompt template across many topics.

---

#### 🧰 Tips for Using Messages Effectively

| Tip 💡                          | Why it Helps                                       |
|---------------------------------|----------------------------------------------------|
| Start with a **system message** | Set the tone/role for the assistant                |
| Use **few-shot examples**       | Teach the model by showing good responses          |
| Use **clear user prompts**      | Make it obvious what you want from the model       |
| Use variables `{}`              | Make templates reusable and dynamic                |

---

####  You Can Combine with Output Parsers!

```python
chain = prompt | llm| output_parser
response = chain.invoke({"topic": "honey bees"})
```


Ah! Got it—you’re asking about the actual **message classes** in LangChain like `HumanMessage`, `AIMessage`, `SystemMessage`, etc. Perfect! These are the **building blocks** of chat-based prompts.

Let’s dive deep 👇

---

### 💬 What are `HumanMessage`, `AIMessage`, `SystemMessage`?

These are **Python classes** in LangChain that represent different types of chat messages in a conversation. They are part of `langchain_core.messages`.

#### 📦 Import them like this:
```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
```

---

#### 🧱 What Each Message Means

| Class           | Role     | Description |
|------------------|----------|-------------|
| `SystemMessage` | system   | Sets the behavior of the assistant (like "You are a helpful tutor") |
| `HumanMessage`  | user     | Represents what the **human/user** says |
| `AIMessage`     | assistant| Represents what the **AI model** responds with |

> These mirror OpenAI’s `ChatCompletion` message structure.

---

#### 🧪 Example: Building Messages Manually

```python
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI()

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What's the capital of Japan?")
]

response = chat(messages)
print(response.content)
# Output: Tokyo
```

> This is the **lowest level** usage. You build the message list yourself.

---

#### 🧠 When to Use These Classes Directly

Use these when:
- You want **fine-grained control** over each message in the conversation.
- You're building **chat history** manually.
- You're not using `ChatPromptTemplate`, but still using `ChatOpenAI`.

---

#### 🧩 Example: Multi-Turn Conversation with AIMessage

```python
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is 2 + 2?"),
    AIMessage(content="2 + 2 equals 4."),
    HumanMessage(content="What is 3 * 3?")
]

response = chat(messages)
print(response.content)
# Output: 9
```

This is how you do **few-shot examples** without using `ChatPromptTemplate`.

---

#### 🧰 Comparison with `ChatPromptTemplate`

| You Use...            | When You Want...                                |
|-----------------------|--------------------------------------------------|
| `ChatPromptTemplate`  | Dynamic templates with placeholders              |
| `HumanMessage`, etc.  | Full control over individual message construction |

---

#### 🧠 Recap

```python
from langchain.schema import HumanMessage, AIMessage, SystemMessage

HumanMessage(content="Hello, what can you do?")
AIMessage(content="I can help you with any questions.")
SystemMessage(content="You are a friendly assistant.")
```

These are used:
- directly with `ChatOpenAI`
- or inside `ChatPromptTemplate` (LangChain wraps them under the hood!)


#### ChatPromptTemplate 

```python 
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Tell me a fun fact about spiders.")
])

formatted_messages = prompt.format_messages()

```
#### Manually (Messages)
```python
from langchain.schema import HumanMessage, AIMessage, SystemMessage
formatted_messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What's the capital of Japan?")
]
```
----


## Best Practice for Prompting



#### ⚔️ `ChatPromptTemplate` vs Manual `HumanMessage` / `SystemMessage`

| Feature                        | `ChatPromptTemplate` ✅ | Manual Messages (e.g. `HumanMessage`) |
|-------------------------------|--------------------------|----------------------------------------|
| 🔄 Dynamic variable injection  | ✅ Automatic              | ❌ Manual (`.format()` / f-strings)    |
| 🧼 Cleaner syntax              | ✅ Yes                   | ❌ Gets messy in large chains          |
| 🧰 Output parser integration   | ✅ Built-in friendly      | ❌ Manual output parsing               |
| 🔁 Reusability in chains       | ✅ Easy to pipe into chains | ⚠️ Needs boilerplate code             |
| 🧠 Used by LangChain agents    | ✅ Core of agent system   | ❌ Not easily pluggable               |
| 🧩 Works well with memory      | ✅ Yes                   | ⚠️ You’ll need to manage history       |
| 📦 Multi-message support       | ✅ Built-in               | ✅ But more verbose                    |

---

### ✅ **Recommended for Professional Projects:**
#### → **Use `ChatPromptTemplate`**

#### 🧠 Why?

1. **Scales cleanly** as prompts grow in complexity  
2. Built-in support for:
   - memory
   - format instructions
   - agents
   - dynamic injection
3. Easier to collaborate with teams (clear variable naming)
4. Works well with all `LCEL` (LangChain Expression Language) pipelines
5. Better compatibility with **LangServe**, **FastAPI**, or when deploying

---

### 🛠 Pro Tip: Use Manual Messages Only When...

- You need **complete control** over message history (e.g., simulating a real chat interface)
- You’re working **outside LangChain** (e.g., calling OpenAI API directly)
- You’re doing quick prototyping

---

#### ✅ Final Verdict

| Use Case                         | Best Approach          |
|----------------------------------|------------------------|
| Clean, professional LLM pipeline | `ChatPromptTemplate` ✅ |
| Building reusable components     | `ChatPromptTemplate` ✅ |
| One-off, hardcoded calls         | `HumanMessage` / manual |
| Full chat simulation             | Manual + ChatModel     |

---

## Model Input Few-shot Prompting
Providing the LLM with a few such examples is called few-shotting, and is a simple yet powerful way to guide generation and in some cases drastically improve model performance.
For more complex schemas it's very useful to add few-shot examples to the prompt. This can be done in a few ways.

The simplest and most universal way is to add examples to a system message in the prompt:

```python

from langchain_core.prompts import ChatPromptTemplate

system = """You are a hilarious comedian. Your specialty is knock-knock jokes. \
Return a joke which has the setup (the response to "Who's there?") and the final punchline (the response to "<setup> who?").

Here are some examples of jokes:

example_user: Tell me a joke about planes
example_assistant: {{"setup": "Why don't planes ever get tired?", "punchline": "Because they have rest wings!", "rating": 2}}

example_user: Tell me another joke about planes
example_assistant: {{"setup": "Cargo", "punchline": "Cargo 'vroom vroom', but planes go 'zoom zoom'!", "rating": 10}}

example_user: Now about caterpillars
example_assistant: {{"setup": "Caterpillar", "punchline": "Caterpillar really slow, but watch me turn into a butterfly and steal the show!", "rating": 5}}"""

prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")])

few_shot_structured_llm = prompt | structured_llm
few_shot_structured_llm.invoke("what's something funny about woodpeckers")

```


## Model output Parsing
## Model output Cacheing 
