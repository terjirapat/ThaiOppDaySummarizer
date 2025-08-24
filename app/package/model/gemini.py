import yaml
from google import genai
from package.prompts import Prompt

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

client = genai.Client(api_key=config['GEMINI_API_KEY'])

def query_gemini(prompt: Prompt, user_prompt) -> str:
    response = client.models.generate_content(
        model=prompt.model_name, 
        contents=f'{prompt.system_prompt}/n {user_prompt}',
        config=genai.types.GenerateContentConfig(
            temperature=0,
            # thinking_config=genai.types.ThinkingConfig(thinking_budget=0)
        ),
    )
    return response.text