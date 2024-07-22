# DeepHyperion+SaFliTe


## Installation and Usage

1. Navigate to the DeepHyperion+SaFliTe_Chatgpt3.5 or DeepHyperion+SaFliTe_mistral folder:
    ```bash
    cd DeepHyperion+SaFliTe_Chatgpt3.5
    ```
	or
	
	```bash
    cd DeepHyperion+SaFliTe_mistral
    ```
	
2. If you want to run DeepHyperion+SaFliTe_mistral, you need to first download the Mistral model from the following URL:
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF 

	Create a folder named **LLM_model** in the **DeepHyperion+SaFliTe_mistral** directory and Place the downloaded model in the **LLM_model** folder


3. Create a Docker Image:
	```bash
    sudo docker build -t [YOUR_IMAGE_NAME] .
    ```

4. Setting .env file:
	```bash
    cd ..
	vim .env
    ```
	```plaintext
	# .env file

	# Add your ChatGPT API key here
	chatGPT_api_key=YOUR_API_KEY
	
	#Change your ChatGPT model
	chatGPT_model=GPT_MODEL

5. Run the Docker container:
	```bash
    sudo docker run --env-file .env -dit [YOUR_IMAGE_NAME]

	sudo docker exec -it [CONTAINER_ID] bash
    ```
	
6. Run the generator:
	```bash
    python3 cli.py generate case_studies/mission2.yaml 200
    ```



