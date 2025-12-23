from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class QPaginationSchema(BaseSchema):
    page: Annotated[Optional[int], Field(default=1, ge=1, description="Page number")]
    limit: Annotated[Optional[int], Field(default=10, description="Page number")]
