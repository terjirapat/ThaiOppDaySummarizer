import ollama
from abc import ABC, abstractmethod
from package.prompt import Prompt

class ModelRunner(ABC):
    @abstractmethod
    def run(self, prompt: Prompt) -> str:
        pass

class OllamaRunner(ModelRunner):
    def run(self, prompt: Prompt) -> str:
        response = ollama.chat(
            model=prompt.model_name,
            messages=[
                {"role": "system", "content": prompt.system_prompt},
                {"role": "user", "content": prompt.user_prompt}
            ],
            options={
                "temperature": 0
            }
        )   
        return response["message"]["content"]

class ModelManager:
    def __init__(self):
        self.runners = {}

    def register_runner(self, model_name: str, runner: ModelRunner):
        self.runners[model_name] = runner

    def run(self, prompt: Prompt) -> str:
        if prompt.model_name not in self.runners:
            raise ValueError(f"No runner registered for {prompt.model_name}")
        return self.runners[prompt.model_name].run(prompt)