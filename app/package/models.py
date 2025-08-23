import ollama
from pydantic import BaseModel

class Prompt(BaseModel):
    model_name: str
    system_prompt: str

def query_ollama(prompt: Prompt, user_prompt: str) -> str:
    response = ollama.chat(
        model=prompt.model_name,
        messages=[
            {"role": "system", "content": prompt.system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        options={
            "temperature": 0
        }
    )   
    return response["message"]["content"]