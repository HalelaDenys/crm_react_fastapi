from schemas.base_schema import BaseSchema
from datetime import datetime
from pydantic import Field
from typing import Annotated


class CreateCategorySchema(BaseSchema):
    name: Annotated[str, Field(min_length=3, max_length=50)]


class ReadCategorySchema(CreateCategorySchema):
    id: int
    created_at: datetime
