# SOP: Automated Test Case Generation

## 1. Goal
Generate structured test cases (JSON) from a natural language feature description using a local LLM (Ollama).

## 2. Inputs
- **Feature Description** (String): The user's requirement.
- **Model** (String, default=`llama3.2`): The LLM to use.

## 3. Logic (The "Thinking" Process)
1.  **Receive Input**: Accept the feature description.
2.  **Construct Prompt**:
    - Role: "You are a Senior QA Automation Engineer."
    - Task: "Generate comprehensive test cases for the following feature."
    - Constraint: "Output MUST be valid JSON matching the defined schema."
    - Format: Provide a 1-shot example of the desired JSON structure.
3.  **Invoke LLM**: Call `ollama.chat` with the constructed prompt.
4.  **Parse & Validate**:
    - Extract JSON from the response.
    - Validate against the schema (using Pydantic in the implementation).
    - If JSON is malformed, retry (optional, simplistic version just errors).
5.  **Output**: Return the validated JSON object.

## 4. Edge Cases
- **Empty Input**: Return error "Feature description cannot be empty."
- **LLM Failure**: If Ollama is down, return 503 "Service Unavailable."
- **Malformed JSON**: If LLM outputs text/markdown instead of JSON, attempt to strip code blocks, else return error.

## 5. Tool Interface
The implementing tool `tools/generate_test_cases.py` should expose a function:
`generate_tests(prompt: str, model: str = "llama3.2") -> Dict`
