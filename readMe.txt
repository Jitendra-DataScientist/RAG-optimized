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
