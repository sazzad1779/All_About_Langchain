from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-3.5-turbo-0125",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
