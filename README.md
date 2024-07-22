# SaFliTe
## Installing Dependencies

To install the necessary dependencies for SaFliTe, navigate to the SaFliTe folder and run the following command:

```sh
pip install -r requirements.txt
```

## Run SaFliTe

To run SaFliTe, use the following command:

```sh
python SaFliTe.py --test_cases [path to test_cases file] --current_state [path to current_state file] --def_of_int [path to definition_of_interestingness file]
```
Replace [path to test_cases file], [path to current_state file], and [path to definition_of_interestingness file] with the actual paths to your test cases, current state, and definition of interestingness files, respectively.

## Choose a Different LLM

By default, SaFliTe uses ChatGPT3.5 for analysis. If you want to use the Mistral-7B model, follow these steps:

1. Download the Mistral-7B model from the following URL: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF

2. Create a folder named **local_model** in the SaFliTe directory:
	```sh
	mkdir local_model
	```

3. Place the downloaded model in the **local_model** folder.

4. Run the following command:
	```sh
	python SaFliTe.py --test_cases [path to test_cases file] --current_state [path to current_state file] --def_of_int [path to definition_of_interestingness file] --LLM Mistral-7B
	```

## SaFliTe-Enhanced Fuzzing Tool
To run the SaFliTe-enhanced Fuzzing Tool, refer to the detailed instructions available in the respective Fuzzing Tool folder. 