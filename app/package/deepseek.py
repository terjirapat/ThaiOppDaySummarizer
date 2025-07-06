import requests
import yaml


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# --- CONFIG ---
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = config['api_key_deepseek_r1_0528']
MODEL_NAME = "deepseek/deepseek-r1-0528:free"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def initialize_conversation():
    """
    Initialize the conversation with a system prompt.

    Returns:
        list: A list containing the initial system message for the conversation history.
    """
    return [{"role": "system", "content": "You are a helpful assistant."}]


def get_user_input():
    """
    Prompt the user for input.

    Returns:
        str: The user input as a string.
    """
    return input(">>> ")


def generate_response(messages):
    """
    Send the conversation history to the DeepSeek model via OpenRouter
    and return the assistant's reply.

    Args:
        messages (list): The list of all messages in the conversation so far.

    Returns:
        str: The assistant's reply.
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    assistant_reply = response.json()["choices"][0]["message"]["content"]
    print("Assistant:", assistant_reply)
    return assistant_reply


def chat_loop():
    """
    Run the main chat loop. Continues until the user types 'exit'.

    This function handles input/output and maintains the conversation state.
    """
    messages = initialize_conversation()

    while True:
        user_input = get_user_input()
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        assistant_reply = generate_response(messages)
        messages.append({"role": "assistant", "content": assistant_reply})