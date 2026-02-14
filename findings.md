# Findings & Constraints

## Requirements
- **Goal**: Create a local LLM test case generator.
- **Core Technology**: Ollama (Python `ollama` library).

## Research
- **Local LLM Test Generation**:
    - **Library**: `ollama` python library is the standard way to interact. `pip install ollama`.
    - **Methodology**: 
        - Use `ollama.generate` or `ollama.chat` for interaction.
        - **Prompting**: Chain-of-thought (Requirements -> Conditions -> Cases) is effective. Role prompting ("Act as QA Engineer") improves quality.
    - **Libraries**: `LangChain` can be used for complex flows, but `ollama` direct API is sufficient for many cases.
    - **Output**: Can generate functional, unit, or UI automation scripts. Structured output (JSON) is preferred for programmatic use.
    - **Tools**: Existing tools like `AutoTestGen` and `LangExtract` exist but custom implementation gave better control over specific "North Star" requirements.
- **Pending**: User specific prompt for the generator.

## Constraints
- Must run locally using Ollama.
- Privacy: All processing must happen locally.
