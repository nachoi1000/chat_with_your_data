# chat_with_your_data

## Introduction
------------
The MultiPDF Chat App is a Python application that allows you to chat with multiple documents (PDF or TXT documents). You can ask questions about the document using natural language, and the application will provide relevant responses based on the content of the documents or not. This app utilizes a language model to generate accurate answers to your queries. Please note that the app will respond based or not on the document, It will depend on the user prompt. 

## How It Works
------------

![MultiPDF Chat App Diagram]

The application follows these steps to provide responses to your questions:

1. Document Loading: The app reads multiple PDF or TXT documents and extracts their text content.

2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.

3. Embedding and Vectorstore: The application utilizes a large language model to generate vector representations (embeddings) of each text chunks for each document.

4. Similarity Matching: When you ask a question (generate an user prompt), the app compares it prompt with the vectors of each text chunks and retrieves the most semantically similar ones.

5. Response Generation: The selected chunks are passed to the language model as context in a prompt, the large language model will generates a response using the context or not depending on the original user prompt.

## Dependencies and Installation
----------------------------
To install the MultiPDF Chat App, please follow these steps:

1. Clone the repository to your local machine.
2. Generate a python virtual environment and install the required dependencies, feel free to follow these steps:
   ```
   python -m venv name_of_the_virtualenv
   change dir to your local machine repository and execute name_of_the_virtualenv/Scripts/activate
   pip install -r requirements.txt
   ```

3. Obtain an API key from OpenAI and add it to a `secret_keys.py` file in the project directory.
```commandline
OPENAI_API_KEY=your_secrit_api_key
```

## Usage
-----
To use the MultiPDF Chat App, follow these steps:

1. Ensure that you have installed the required dependencies, create `secret_keys.py` and added the OpenAI API key in the file.

2. Run the `main.py` file using the Streamlit CLI. Execute the following command:
   ```
   streamlit run main.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Load multiple documents into the app by following the provided instructions.

5. Ask questions in natural language about the loaded documents using the chat interface.

## Contributing
------------
This repository is intended for educational purposes and does not accept further contributions. Feel free to utilize and enhance the app based on your own requirements.

## Credits
-------
This project has been inspired in https://github.com/alejandro-ao/ask-multiple-pdfs repository.

Special thanks to:

https://www.linkedin.com/in/mat%C3%ADas-alloatti-966b8216a/

https://www.linkedin.com/in/alejandro-trinidad/

https://www.linkedin.com/in/erik-davidsson-54b4848/
