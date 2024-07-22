import openai
import os
import time
import ast
from llama_cpp import Llama

class GPT_object:
    def __init__(self,api_key, init_prompt, model=os.environ.get("chatGPT_model")):
        self.api_key = api_key
        self.model = model
        self.init_prompt = init_prompt
        self.dialogue_history = [{"role": "system", "content": self.init_prompt}]

    def add_message(self, role, content):
        self.dialogue_history.append({"role": role, "content": content})

    def get_response(self, user_input):
        self.add_message("user", user_input)
        openai.api_key = self.api_key
        retries_limit = 12
        while retries_limit != 0:
            try:
                # Try to get model response and return it
                time.sleep(1)
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=self.dialogue_history,
                    temperature=float(os.environ.get("TEMPERATURE")),
                    top_p=float(os.environ.get("TOP_P")),
                )
                model_response = response.choices[0].message.content
                last_line = model_response.strip().split('\n')[-1]
                print("list:", last_line)
                try:
                    last_line_obj = ast.literal_eval(last_line)
                    if isinstance(last_line_obj, list):
                        return last_line_obj.index(max(last_line_obj))
                    else:
                        retries_limit -= 1
                
                except (ValueError, SyntaxError):
                    retries_limit -= 1

            except Exception as e:
                # print(e)
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