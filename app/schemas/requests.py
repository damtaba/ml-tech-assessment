from pydantic import BaseModel, Field, field_validator, StringConstraints
from typing import Annotated
from fastapi import Query


TextToSummary = Annotated[str, StringConstraints(strip_whitespace=True, min_length=10)]