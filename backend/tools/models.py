from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union, Dict, Any

class TestCase(BaseModel):
    id: str = Field(..., description="Unique Identifier like TC_001")
    title: str = Field(..., description="Short title of the test case")
    description: str = Field(..., description="Detailed description")
    preconditions: List[str] = Field(default_factory=list, description="List of preconditions")
    steps: List[str] = Field(..., description="Step-by-step instructions")
    expected_result: str = Field(..., description="The expected outcome")
    priority: str = Field(..., description="Priority: High, Medium, Low")
    type: str = Field(..., description="Type: Positive, Negative, Boundary, etc.")

    @field_validator('steps', mode='before')
    @classmethod
    def parse_steps(cls, v: List[Any]) -> List[str]:
        cleaned = []
        for step in v:
            if isinstance(step, str):
                cleaned.append(step)
            elif isinstance(step, dict):
                # Try to extract the description from common keys the LLM might use
                # Based on error: {'step_id': '...', 'step_description': '...'}
                desc = step.get('step_description') or step.get('description') or step.get('step') or step.get('text')
                if desc:
                    cleaned.append(str(desc))
                else:
                    # Fallback to string representation if no clear text field
                    cleaned.append(str(step))
            else:
                cleaned.append(str(step))
        return cleaned

class TestCaseResponse(BaseModel):
    test_cases: List[TestCase]
