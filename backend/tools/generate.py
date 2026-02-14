import ollama
import json
from typing import Dict, Any
from tools.models import TestCaseResponse

MODEL_NAME = "llama3.2:latest"

SYSTEM_PROMPT = """
You are an expert QA Automation Engineer.
Your task is to generate comprehensive test cases based on the user's feature description.
You MUST return the output as valid JSON adhering to the following schema:
{
  "test_cases": [
    {
      "id": "TC_001",
      "title": "...",
      "description": "...",
      "preconditions": ["..."],
      "steps": ["Step 1: Description...", "Step 2: Description..."],
      "expected_result": "...",
      "priority": "High|Medium|Low",
      "type": "Positive|Negative|Boundary"
    }
  ]
}
Do NOT include any markdown formatting (like ```json), just the raw JSON object.
"""

def generate_test_cases(feature_description: str) -> Dict[str, Any]:
    """
    Generates test cases using Ollama (Llama 3.2) and returns a structural dictionary.
    """
    if not feature_description.strip():
        raise ValueError("Feature description cannot be empty.")

    print(f" Generating test cases for: {feature_description[:50]}...")
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': feature_description}
            ],
            options={'temperature': 0.7} # Deterministic creativity
        )
        
        content = response['message']['content']
        
        # Clean up potential markdown formatting
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        content = content.strip()
        
        # Parse and Validate
        data = json.loads(content)
        # Validate with Pydantic
        validated = TestCaseResponse(**data)
        
        return validated.model_dump()

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        print(f"Raw Output: {content}")
        raise ValueError("LLM failed to generate valid JSON.")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise e

if __name__ == "__main__":
    # Test run
    sample = "Login page with email and password."
    try:
        result = generate_test_cases(sample)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Failed: {e}")
