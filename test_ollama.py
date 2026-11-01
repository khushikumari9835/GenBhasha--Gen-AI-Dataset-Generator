import ollama

response = ollama.chat(
    model="qwen2.5:7b",
    messages=[
        {
            "role": "user",
            "content": "Write 5 different natural variations of this sentence in Hindi: राम बाजार जा रहा है।"
        }
    ]
)

print(response["message"]["content"])