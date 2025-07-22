import ollama
from package.chatloop import *

def call_llm(user_prompt: str, system_prompt:str):
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response["message"]["content"]

def main():
    # while True:
    #     user_prompt = input('>>> ')
    #     if user_prompt=='exit':
    #         break
    #     system_prompt = "You are a native english speaker that always rewrite the user’s sentence in natural, fluent English like a native speaker. Keep the meaning. Only output the improved sentence."
    #     response = call_llm(user_prompt=user_prompt, system_prompt=system_prompt)
    #     print(response)
    #     chat_loop(system_prompt="You are a native english speaker that always teching english")
    bot1_system_prompt = "you are a philosopher"
    bot1_message = initialize_conversation(system_prompt=bot1_system_prompt)
    bot1_assistant_reply = generate_response_bot1(bot1_message)
    bot1_message.append({"role": "assistant", "content": bot1_assistant_reply})

    bot2_system_prompt = "you are a Scientist"
    bot2_message = initialize_conversation(system_prompt=bot2_system_prompt)


    n = 0
    while n!=10:
        bot2_message.append({"role": "user", "content": bot1_assistant_reply})
        bot2_assistant_reply = generate_response_bot2(bot2_message)
        bot2_message.append({"role": "assistant", "content": bot2_assistant_reply})

        bot1_message.append({"role": "user", "content": bot2_assistant_reply})
        bot1_assistant_reply = generate_response_bot1(bot1_message)
        bot1_message.append({"role": "assistant", "content": bot1_assistant_reply})

        n += 1



if __name__=="__main__":
    main()