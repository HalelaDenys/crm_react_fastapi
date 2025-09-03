from schemas.base_schema import BaseSchema
from datetime import datetime
from pydantic import Field
from typing import Annotated


class CreatePositionSchema(BaseSchema):
    name: Annotated[str, Field(min_length=3, max_length=50)]


class ReadPositionSchema(CreatePositionSchema):
    id: int
    created_at: datetime
