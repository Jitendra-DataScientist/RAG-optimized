# API Module

# Import the os module
import os

# Filter warnings
import warnings

# Import the FastAPI class from the fastapi module to create the API
from fastapi import FastAPI

# Import the HuggingFaceEmbeddings class from the langchain_huggingface module to generate embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Import the Qdrant class from the langchain_qdrant module to instantiate the vector database
from langchain_qdrant import Qdrant

# Import the BaseModel class from the pydantic module to validate data sent to the API
from pydantic import BaseModel

# Import the QdrantClient class from the qdrant_client module to connect to the vector database
from qdrant_client import QdrantClient

# Import the env_var module containing the LLM API key
# import src.config.env_var as env_var
import config.env_var as env_var

warnings.filterwarnings('ignore')

# Define the Item class that inherits from BaseModel
class Item(BaseModel):
    query: str

# Define the model name (tokenizer)
model_name = "sentence-transformers/msmarco-bert-base-dot-v5"

# Define the model arguments
model_kwargs = {'device': 'cpu'}

# Define the encoding arguments
encode_kwargs = {'normalize_embeddings': True}

# Create an instance of HuggingFaceEmbeddings
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs)


# Set the variable use_nvidia_api to False
use_nvidia_api = False

# Check if the Nvidia key is available
if env_var.nvidia_key != "":

    # Import the OpenAI class from the openai module
    from openai import OpenAI

    # Create an OpenAI instance with the base URL and API key
    client_ai = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=env_var.nvidia_key)

    # Set use_nvidia_api to True
    use_nvidia_api = True

else:

    # Print a message indicating that an LLM cannot be used
    print("It is not possible to use an LLM.")

# Create an instance to connect to the vector database
client = QdrantClient("http://localhost:6333")

# Define the collection name
collection_name = "VectorDB"

# Create a Qdrant instance to send data to the vector database
qdrant = Qdrant(client, collection_name, hf)


# Create an instance
app = FastAPI()

# Define the root route with the GET method
@app.get("/")
async def root():
    return {"message": "Full RAG Qdrant Project"}

# Define the /api route with the POST method
@app.post("/api")
async def api(item: Item):

    # Get the query from the item
    query = item.query

    # Perform similarity search
    search_result = qdrant.similarity_search(query=query, k=3)

    # Initialize the results list, context, and mapping
    list_res = []
    context = ""
    mappings = {}

    # Build the context and results list
    for i, res in enumerate(search_result):
        context += f"{i}\n{res.page_content}\n\n"
        mappings[i] = res.metadata.get("path")
        list_res.append({"id": i, "path": res.metadata.get("path"), "content": res.page_content})

    # Define the system message
    rolemsg = {"role": "system",
               "content": "Answer the user's question using documents provided in the context. The context contains documents that should hold an answer. Always reference the document ID (in brackets, e.g., [0],[1]) of the document used for a query. Use as many citations and documents as needed to answer the question."}

    # Define the messages
    messages = [rolemsg, {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {query}"}]

    # Check if the Nvidia API is being used
    if use_nvidia_api:

        # Create the LLM instance using the Nvidia API
        resposta = client_ai.chat.completions.create(model="meta/llama3-70b-instruct",
                                                     messages=messages,
                                                     temperature=0.5,
                                                     top_p=1,
                                                     max_tokens=1024,
                                                     stream=False)

        # Get the response from the LLM
        response = resposta.choices[0].message.content

    else:

        # Print a message indicating that an LLM cannot be used
        print("It is not possible to use an LLM.")

    return {"context": list_res, "answer": response}
