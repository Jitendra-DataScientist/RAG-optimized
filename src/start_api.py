# API Initialization Module

# Import
import uvicorn

# Initializes the API
if __name__ == "__main__":
    uvicorn.run("api:app", host='0.0.0.0', reload=False, workers=3, port=8003
)
