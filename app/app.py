import yaml
# from package.deepseek import chat_loop

#---------------------------------------------------------

# # load config
# with open("config.yaml", "r") as file:
#     config = yaml.safe_load(file)

#---------------------------------------------------------

def main():
    import requests
    from bs4 import BeautifulSoup

from package.ollama import chat_loop
    url = input('>>>')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string.replace(" - YouTube", "").strip()
    print(title)

if __name__=="__main__":
    main()

    