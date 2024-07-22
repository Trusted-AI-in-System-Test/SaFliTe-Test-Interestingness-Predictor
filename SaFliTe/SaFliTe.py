import argparse
import time

import analysis_agent

def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at {file_path} was not found."
    except IOError:
        return f"Error: Could not read the file at {file_path}."

def check_llm(value):
    valid_llms = ["ChatGPT3.5", "Mistral-7B"]
    if value not in valid_llms:
        raise argparse.ArgumentTypeError(f"Invalid value for --LLM: {value}. Choose from {valid_llms}")
    return value

def main():
    parser = argparse.ArgumentParser(description="The interesting test cases predictor")
    parser.add_argument("--test_cases", default=None, help="test cases file path")
    parser.add_argument("--current_state", default=None, help="current state file path")
    parser.add_argument("--def_of_int", default=None, help="definition of interestingness file path")
    parser.add_argument("--LLM", default="ChatGPT3.5", type=check_llm, help="You can choose ChatGPT3.5 or Mistral-7B.")
    args = parser.parse_args()

    text_cases = read_txt_file(args.test_cases)

    def_of_int = read_txt_file(args.def_of_int)

    current_state = read_txt_file(args.current_state)

    llm_model = args.LLM



    init_prompt = ("We are testing an UAV control system. Based on the current state of UAV， you will serve as a predictor to determine which test case "
                   "is the most interesting.\n"
                   "#Current state of UAV\n" + current_state +
                   "#The definition of interestingness\n" + def_of_int +
                   "\n#test cases\n" + text_cases +
                   "#output format\n"
                   "Attention：You need to output the analysis for each test case！ For each test case, the output should follow "
                   "these chains of thought: First, analyze what the"
                   "test case represents (under the heading 'INTERPRETATION', all caps). Then output just "
                   "the string 'x out of 10' where 'x' is an integer corresponding to how interesting the test case "
                   "is (under the heading 'ANSWER', all caps). Then show a detailed reason for your answer "
                   "(under the heading 'REASON', all caps). Example for a test case: \ntest case 1: xxx\n THINKING\n "
                   "test case represent \n ANSWER\n x out of 10 \n REASON\n REASON\n You need to output the analysis for all test case！"
                   "All scores will be stored in a list in the order of test case and this list wiil be outputted(under the heading 'Score List')"
                   "Your output should end with this score list. The last part of the example for output：\nScore List\n [x,x,x,x,x]")

    LLM_agent = analysis_agent.GPT_object(init_prompt, llm_model)
    print("**************SaFliTe Launch**************\n")

    print("Providing resources to the LLM")

    print("==================================================")

    print("The LLM is analyzing...")

    response = LLM_agent.get_response("Start the analysis")

    print("==================================================")

    print("LLM Analysis Complete")

    with open("LLM_output", 'w') as file:
        file.write(response)

    print("==================================================")
    time.sleep(2)
    print("Results Saved")

    print("==================================================")


if __name__ == '__main__':
    main()
