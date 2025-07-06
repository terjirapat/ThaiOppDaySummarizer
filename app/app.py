import yaml
from package.ollama import chat_loop
# from package.deepseek import chat_loop

#---------------------------------------------------------

# # load config
# with open("config.yaml", "r") as file:
#     config = yaml.safe_load(file)

#---------------------------------------------------------

def main():
    chat_loop()

if __name__=="__main__":
    main()

    