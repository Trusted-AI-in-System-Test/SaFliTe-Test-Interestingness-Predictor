import time
import openai
import ast
from llama_cpp import Llama

openai.api_key = ""

# GPT_VERSION = "gpt-4"
GPT_VERSION = "gpt-3.5-turbo-1106"
TEMPERATURE = 0 # Make output as deterministic as possible
TOP_P = 0 # Make output as deterministic as possible

class GPT_object:
    def __init__(self, init_prompt, model):
        self.model = model
        self.init_prompt = init_prompt
        self.dialogue_history = [{"role": "system", "content": self.init_prompt}]

    def add_message(self, role, content):
        self.dialogue_history.append({"role": role, "content": content})

    def get_response(self, user_input):
        if self.model == "ChatGPT3.5":
            self.add_message("user", user_input)
            retries_limit = 12
            while retries_limit != 0:
                try:
                    # Try to get model response and return it
                    time.sleep(1)
                    response = openai.chat.completions.create(
                        model=GPT_VERSION,
                        messages=self.dialogue_history,
                        temperature=TEMPERATURE,
                        top_p=TOP_P,
                    )
                    model_response = response.choices[0].message.content
                    last_line = model_response.strip().split('\n')[-1]

                    try:
                        last_line_obj = ast.literal_eval(last_line)
                        if isinstance(last_line_obj, list):
                            return model_response
                        else:
                            retries_limit -= 1

                    except (ValueError, SyntaxError):
                        retries_limit -= 1

                except Exception as e:
                    print(e)
                    if str(e).startswith("This model's maximum context length"):
                        # Tokens per minute rate has not been exceeded, just message itself is too long to input
                        self.dialogue_history.pop(-1)
                        return -1
                    # Most likely tokens per minute rate has been exceeded so wait a little and try again
                    time.sleep(10)
                    retries_limit -= 1

            # Max retries exceeded, still have no response
            self.dialogue_history.pop(-1)
            return -2

        if self.model == "Mistral-7B":
            llm = Llama(model_path="local_model/mistral-7b-instruct-v0.2.Q5_K_M.gguf",
                        chat_format="llama-2", n_ctx=32768, n_threads=8)
            self.add_message("user", user_input)
            retries_limit = 12
            while retries_limit != 0:
                try:
                    generate_output = llm.create_chat_completion(messages=self.dialogue_history)
                    output_string = generate_output["choices"][0]["message"]["content"]
                    last_line = output_string.strip().split('\n')[-1]

                    try:
                        last_line_obj = ast.literal_eval(last_line)
                        if isinstance(last_line_obj, list):
                            return output_string
                        else:
                            retries_limit -= 1

                    except (ValueError, SyntaxError):
                        retries_limit -= 1


                except Exception as e:
                    # Message must be too long (or out of memory)
                    print(["error", e])
                    time.sleep(10)
                    retries_limit -= 1

            # output_string = generate_output["choices"][0]["message"]["content"]
            # self.add_message("assistant", output_string)
            self.dialogue_history.pop(-1)
            return -2