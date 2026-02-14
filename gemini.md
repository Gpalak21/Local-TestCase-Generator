# Project Constitution (Gemini)

## 1. Project Overview
A local web-based Test Case Generator using Ollama (Llama 3.2). Users input feature requirements via a chat interface, and the system outputs structured test cases using a predefined template.

## 2. Data Schemas

### Core Entity: `TestCase`
The LLM will be instructed to output data adhering to this JSON structure:

```json
{
  "test_cases": [
    {
      "id": "TC_001",
      "title": "Verify user login with valid credentials",
      "description": "Ensure that a registered user can log in successfully with correct username and password.",
      "preconditions": [
        "User is registered",
        "Login page is open"
      ],
      "steps": [
        "Enter valid username",
        "Enter valid password",
        "Click Login button"
      ],
      "expected_result": "User is redirected to the dashboard.",
      "priority": "High",
      "type": "Positive"
    }
  ]
}
```

### API Payload (Frontend <-> Backend)
**Request:**
```json
{
  "prompt": "User requirement text..."
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "test_cases": [ ... ] 
  }
}
```

## 3. Behavioral Rules
- **Privacy First**: All data processing must happen locally via Ollama. No external API calls for inference.
- **Deterministic Structure**: Output must strictly follow the JSON schema. Randomness in *format* is not allowed, though creative *content* is encouraged.
- **Model**: Default to `llama3.2` (or user configured model).
- **Interface**: A "Wow" factor web chat interface (HTML/JS/CSS) that feels premium.

## 4. Architectural Invariants
- **Backend**: Python (FastAPI/Flask) to interface with Ollama.
- **Frontend**: Vanilla HTML/CSS/JS for maximum design control.
- **LLM Provider**: Ollama (Running locally).
