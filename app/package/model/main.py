from abc import ABC, abstractmethod
from package.prompts import Prompt
from package.model.ollama import query_ollama
from package.model.gemini import query_gemini


class ModelRunner(ABC):
    @abstractmethod
    def run(self, prompt: Prompt) -> str:
        pass

class OllamaRunner(ModelRunner):
    def run(self, prompt: Prompt, user_prompt) -> str:
        return query_ollama(prompt=prompt, user_prompt=user_prompt)
    
class GeminiRunner(ModelRunner):
    def run(self, prompt: Prompt, user_prompt) -> str:
        return query_gemini(prompt=prompt, user_prompt=user_prompt)

class ModelManager:
    def __init__(self):
        self.runners = {}

    def register_runner(self, model_name: str, runner: ModelRunner):
        self.runners[model_name] = runner

    def run(self, prompt: Prompt, user_prompt) -> str:
        if prompt.model_name not in self.runners:
            raise ValueError(f"No runner registered for {prompt.model_name}")
        return self.runners[prompt.model_name].run(prompt=prompt, user_prompt=user_prompt)