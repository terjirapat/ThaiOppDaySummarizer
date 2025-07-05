import yaml
from openai import OpenAI

#---------------------------------------------------------

# load config
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

#---------------------------------------------------------

# client = OpenAI(
#   api_key=config['api_key']
# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user", "content": "write a haiku about ai"}
#   ]
# )

# print(completion.choices[0].message);

def main():
    print('ter')
    print(config['api_key'])

if __name__=="__main__":
    main()