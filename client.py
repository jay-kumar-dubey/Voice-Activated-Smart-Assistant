from openai import OpenAI
#pip install openai
#client = OpenAI()
#defaults to getting the key using os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key="#####"
)

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant name 'Jarvis' skilled in verbal communication with user and assisting them."},
        {
            "role": "user", "content": "What is Programming."
        }
    ]
)

print(completion.choices[0].message.content)
