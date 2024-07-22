import os
import time
import ast
from llama_cpp import Llama

llm = Llama(model_path="/src/DeepHyperion/LLM_model/mistral-7b-instruct-v0.2.Q5_K_M.gguf", chat_format="llama-2", n_ctx=32768, n_threads=8)


class GPT_object:
    def __init__(self, init_prompt):

        self.init_prompt = init_prompt
        self.dialogue_history = [{"role": "system", "content": self.init_prompt}]

    def add_message(self, role, content):
        self.dialogue_history.append({"role": role, "content": content})

    def get_response(self, user_input):
        self.add_message("user", user_input)
        retries_limit = 12
        while retries_limit != 0:
            try:
                generate_output = llm.create_chat_completion(messages=self.dialogue_history)
                output_string = generate_output["choices"][0]["message"]["content"]
                last_line = output_string.strip().split('\n')[-1]
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
                # Message must be too long (or out of memory)
                print(["error", e])
                time.sleep(10)
                retries_limit -= 1

        # output_string = generate_output["choices"][0]["message"]["content"]
        # self.add_message("assistant", output_string)
        self.dialogue_history.pop(-1)
        return -2


if __name__ == "__main__":
    agent = GPT_object(init_prompt="you are a writer")

    response = agent.get_response("tell me a joke")
    print(response)

        # retries_limit = 12
        # while retries_limit != 0:
        #     try:
        #         # Try to get model response and return it
        #         time.sleep(1)
        #         response = llm.create_chat_completion(
        #             max_tokens=300,
        #             messages=self.dialogue_history,
        #             temperature=1,
        #             top_p=0.95,
        #         )
        #         model_response = response["choices"][0]["message"]["content"]
        #         last_line = model_response.strip().split('\n')[-1]
        #         print("list:", last_line)
        #         try:
        #             last_line_obj = ast.literal_eval(last_line)
        #             if isinstance(last_line_obj, list):
        #                 return last_line_obj.index(max(last_line_obj))
        #             else:
        #                 retries_limit -= 1
        #
        #         except (ValueError, SyntaxError):
        #             retries_limit -= 1
        #
        #     except Exception as e:
        #         # print(e)
        #         if str(e).startswith("This model's maximum context length"):
        #             # Tokens per minute rate has not been exceeded, just message itself is too long to input
        #             self.dialogue_history.pop(-1)
        #             return -1
        #         # Most likely tokens per minute rate has been exceeded so wait a little and try again
        #         time.sleep(10)
        #         retries_limit -= 1
        #
        # # Max retries exceeded, still have no response
        # self.dialogue_history.pop(-1)
        # return -2