from schemas.base_schema import BaseSchema
from datetime import datetime
from pydantic import Field
from typing import Annotated, Optional


class CreateServiceSchema(BaseSchema):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    duration_minutes: Annotated[Optional[int], Field(ge=1, le=999)] = 45
    price: Annotated[int, Field(ge=1, le=999999)]
    category_id: Annotated[int, Field(ge=1)]


class ReadServiceSchema(CreateServiceSchema):
    id: int
    created_at: datetime
