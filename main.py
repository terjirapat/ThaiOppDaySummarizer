import yaml
from package.ollama import *

#---------------------------------------------------------

# load config
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

#---------------------------------------------------------

def main():
    print('test')
    prompt="what does I said previously?"
    run_llama3(prompt=prompt)

if __name__=="__main__":
    main()

    