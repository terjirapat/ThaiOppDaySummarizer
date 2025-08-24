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


import yaml
from google import genai

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

client = genai.Client(api_key=config['GEMINI_API_KEY'])

def query_gemini(prompt: Prompt, user_prompt: str) -> str:
    generation_config = genai.types.GenerationConfig(
        system_instruction=prompt.system_prompt,
        temperature=0,
    )
    response = client.models.generate_content(
        model=prompt.model_name,
        contents=user_prompt,
        generation_config=generation_config,
    )
    return response.text