# TUMB+SaFliTe


## Installation and Usage

1. Navigate to the snippets folder:
    ```bash
    cd TUMB+SaFliTe_Chatgpt3.5/snippets
    ```

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



