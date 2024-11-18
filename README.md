# RAG App
This Streamlit-based Retrieval-Augmented Generation (RAG) app processes uploaded documents, retrieves relevant content for user queries, and provides accurate responses using a Large Language Model (LLM). The app enables seamless document chunking, embedding storage in Chroma Vector Database, and dynamic prompt construction with a compression mechanism for efficient LLM interactions.

## Features :
- **User-Friendly Interface:** Streamlit-based app for easy interaction and intuitive design.

- **Document Upload:** Supports PDF and TXT formats for document processing.

- **Chunking and Embedding:** Splits documents into smaller sections and creates embeddings for storage.

- **Chroma Vector Database:** Efficiently stores and retrieves embeddings for similarity-based queries.

- **Prompt Compression:** Summarizes retrieved chunks to optimize token usage and ensure concise, context-aware prompts.

- **Dynamic Query Handling:** Constructs personalized prompts by combining user queries with relevant document content.

- **LLM Integration:** Leverages advanced LLMs to provide accurate and context-sensitive responses.


## Requirements

- Python 3.12.7

#### Install Python using Anaconda

1) Download and install Anaconda from [here](https://www.anaconda.com/download/success)

2) Create a new environment using the following command:

```bash
conda create -n Rag-app python=3.12.7
```

3) Activate the environment:

```bash
conda activate Rag-app
```

## Installation

### Install the required packages

```bash
pip install -r requirements.txt
```
### Setup the environment variables
Copy the example environment file and set your variables:
```bash
cp .env.example .env
```

Edit the .env file and configure the required environment variables, such as :

```bash
GOOGLE_API_KEY=<your-google-api-key>
```
## How to Start the App :
1- **Ensure your environment is activated:**
```bash
conda activate Rag-app
```
2- **Run FastAPI Server:**
```bash
uvicorn main:app --reload
```
3- **Run the Streamlit App:**
```bash
streamlit run streamlit.py
```
4- **Access the app in your browser:**
- Once the command is executed, the app will automatically open in your default web browser.

- if not, copy the link provided in the terminal and paste it into your browser.

## License:
This project is licensed under the MIT License.

## Contact:
[Mohamed samy](https://www.linkedin.com/in/mohamed-samy02/)