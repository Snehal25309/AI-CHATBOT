import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Hello, introduce yourself in one sentence."
        }
    ]
)

print(response["message"]["content"])