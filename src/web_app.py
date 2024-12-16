# Web Interface and API Query Module

# Import the json module
import json

# Import the re module for regular expressions
import re

# Filter warnings
import warnings

# Import the requests module
import requests

# Import the streamlit module with the alias st
import streamlit as st

warnings.filterwarnings('ignore')

# Configuring the page title and other settings (favicon)
st.set_page_config(page_title="Full RAG Qdrant Project", page_icon=":100:", layout="centered")

# Set the title of the Streamlit application
st.title('_:green[RAG Search]_')
st.title('_:blue[Search with Generative AI and RAG]_')

# Create a text box for entering questions
question = st.text_input("Enter a Question for the AI to Query Documents:", "")


# Check if the "Submit" button has been clicked
if st.button("Submit"):

    # Display the submitted question
    st.write("The submitted question was: \"", question+"\"")

    # Define the API URL
    url = "http://127.0.0.1:8003/api"

    # Create the request payload in JSON format
    payload = json.dumps({"query": question})

    # Define the request headers
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    # Send the POST request to the API
    response = requests.request("POST", url, headers=headers, data=payload)

    # Retrieve the API response and extract the answer text
    try:
        answer = json.loads(response.text)["answer"]
    except:
        print (f"\n\n\n{response.text}\n\n\n\n")

    # Compile a regular expression to find document references
    rege = re.compile("\[Document\ [0-9]+\]|\[[0-9]+\]")

    # Find all document references in the response
    m = rege.findall(answer)

    # Initialize a list to store the document numbers
    num = []

    # Extract the document numbers from the found references
    for n in m:
        num = num + [int(s) for s in re.findall(r'\b\d+\b', n)]

    # Display the answer using markdown
    st.markdown(answer)

    # Retrieve the documents from the response context
    documents = json.loads(response.text)['context']

    # Initialize a list to store the documents to be displayed
    show_docs = []

    # Add the documents corresponding to the extracted numbers to the show_docs list
    for n in num:
        for doc in documents:
            if int(doc['id']) == n:
                show_docs.append(doc)

    # Initialize a variable for the download button identifiers
    bt_id = 17329398437639 

    # Display the expanded documents with download buttons
    for doc in show_docs:

        # Create an expander for each document
        with st.expander(str(doc['id'])+" - "+doc['path']):

            # Display the document content
            st.write(doc['content'])

            # Open the document file and create a download button
            with open(doc['path'], 'rb') as f:

                st.download_button("Download File", f, file_name = doc['path'].split('/')[-1], key = bt_id)

                # Increment the identifier for the download button
                bt_id = bt_id + 1
