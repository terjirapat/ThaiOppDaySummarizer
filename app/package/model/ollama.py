import ollama
from package.prompts import Prompt

def query_ollama(prompt: Prompt, user_prompt: str) -> str:
    response = ollama.chat(
        model=prompt.model_name,
        messages=[
            {"role": "system", "content": prompt.system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        options={
            "temperature": prompt.temperature
        }
    )   
    return response["message"]["content"]