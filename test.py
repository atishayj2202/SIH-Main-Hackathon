# main.py
from langchain.chains.question_answering.map_reduce_prompt import messages

from model import Model
from model.config import SYSTEM_PROMPT, SYSTEM_PROMPT_2

model = Model()

if __name__ == "__main__":
    i = input("input: ")
    if i == "1":
        chat_history = []
        def prompt_func(chat_history):

            prompt = input("You: ")
            output = model.rag_question(
                prompt,
                chat_history
            )
            chat_history.append({"role": "user", "content": prompt})
            chat_history.append({"role": "assistant", "content": output["answer"]})
            print(output["answer"], "\n\n Sources: ", output["sources"])
            prompt_func(chat_history)
        prompt_func(chat_history)
    elif i == "2":
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT_2
                    }
                ]
            }
        ]
        def prompt_func(messages):
            prompt = input("You: ")
            if prompt:
                output = model.global_model(question=prompt, messages=messages)
                print(output)
                messages.append({"role": "assistant", "content": output})
                if output:
                    prompt_func(messages)

        prompt_func(messages)