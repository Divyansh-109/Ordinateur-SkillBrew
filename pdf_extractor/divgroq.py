from groq import Groq

client = Groq(api_key="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")

def llmCall(query):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        temperature=1.0,
    )
    return response.choices[0].message.content.strip()

prompt = input("Enter your prompt: ")
result = llmCall(prompt)
print("LLM Response:", result)