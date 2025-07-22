import ollama

def initialize_conversation(system_prompt:str):
    """
    Initialize the conversation with a system prompt.

    Returns:
        list: A list containing the initial system message for the conversation history.
    """
    return [{"role": "system", "content": system_prompt}]

def generate_response(messages):
    """
    Send the conversation history to the Llama 3 model and return the assistant's reply.

    Args:
        messages (list): The list of all messages in the conversation so far.

    Returns:
        str: The assistant's reply.
    """
    response = ollama.chat(model="llama3", messages=messages)
    assistant_reply = response["message"]["content"]
    print("Assistant:", assistant_reply)
    return assistant_reply


def generate_response_bot1(messages):
    """
    Send the conversation history to the Llama 3 model and return the assistant's reply.

    Args:
        messages (list): The list of all messages in the conversation so far.

    Returns:
        str: The assistant's reply.
    """
    response = ollama.chat(model="llama3", messages=messages)
    assistant_reply = response["message"]["content"]
    print("Bot1:", assistant_reply)
    return assistant_reply

def generate_response_bot2(messages):
    """
    Send the conversation history to the Llama 3 model and return the assistant's reply.

    Args:
        messages (list): The list of all messages in the conversation so far.

    Returns:
        str: The assistant's reply.
    """
    response = ollama.chat(model="llama3", messages=messages)
    assistant_reply = response["message"]["content"]
    print("Bot2:", assistant_reply)
    return assistant_reply

def chat_loop(system_prompt:str):
    """
    Run the main chat loop. Continues until the user types 'exit'.

    This function handles input/output and maintains the conversation state.
    """
    messages = initialize_conversation(system_prompt=system_prompt)

    while True:
        user_input = input(">>> ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        assistant_reply = generate_response(messages)
        messages.append({"role": "assistant", "content": assistant_reply})
