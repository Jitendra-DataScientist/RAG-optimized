Sprint - 1
----------

modified this repo for optimisation:
https://github.com/Jitendra-DataScientist/RAG/

1. reference documents' contents not to be sent in response to save context window.
2. used NVIDEA's meta/llama-3.3-70b-instruct model instead of meta/llama3-70b-instruct.
3. increased max_tokens from 1024 to 128000.
4. listing unique source documents (duplicacies removed).
5. source documents' contents not to be shown on streamlit UI.



Sprint - 2
----------

modifications from Sprint - 1:

changes in code:
----------------
1. changed api.py to take "industry" in payload of /api route to go to particular collection in Qdrant vector DB. Data is now fetched from particular industry's collection.
2. changed api.py to increase timeout to 60 seconds of QdrantClient.
3. changed "rag.py" to create collections in Qdrant vector DB based on industries.
4. changed "web_app.py" to add a industry drop-down to take "industry" key in payload.


changes in CLI:
---------------
1. docker run using:
docker run --name vectordb -dit -p 6333:6333 \
  --cpus="4" \
  --memory="4g" \
  qdrant/qdrant

instead of:
docker run --name vectordb -dit -p 6333:6333 qdrant/qdrant

2. check stats using:
docker stats



Sprint - 3
----------

modifications from Sprint - 2:

changes in code:
----------------
1. changed k-value of similarity_search in "api.py" to 5 from 3.
2. changed the prompt to not cite source documents in the answer itself.
3. changed some formattings in "web_app.py".
