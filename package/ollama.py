import ollama

def run_llama3(prompt):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    print(response["message"]["content"])
    # return result.stdout.strip()

# output = run_llama3("What is the meaning of life?")
# print(output)
