
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

from tools.generate import generate_test_cases
from tools.models import TestCaseResponse

app = FastAPI(title="Local LLM Test Case Generator")

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FeatureRequest(BaseModel):
    feature_description: str
    model: str = "llama3.2"

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Test Case Generator API is running."}

@app.post("/generate", response_model=TestCaseResponse)
def generate_endpoint(request: FeatureRequest):
    """
    Generate test cases based on feature description.
    """
    try:
        # Layer 2: Routing to Tool Layer
        result = generate_test_cases(request.feature_description)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate test cases: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
