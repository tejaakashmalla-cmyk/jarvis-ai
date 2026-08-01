import time
import ollama

model = "qwen2.5:3b"

while True:

    prompt = input("You: ")

    if prompt.lower() == "exit":
        break

    start = time.time()

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    end = time.time()

    print("\nQwen:\n")

    print(response["message"]["content"])

    print(f"\nTime: {end-start:.2f} sec\n")