import re
from datetime import datetime

from schemas.base_schema import BaseSchema
from pydantic import Field, field_validator
from typing import Annotated, Optional, Literal
from datetime import date


class UserSchema(BaseSchema):
    first_name: Annotated[
        str, Field(min_length=4, max_length=50, description="First name user")
    ]
    last_name: Annotated[
        str, Field(min_length=4, max_length=50, description="Last name user")
    ]
    phone_number: Annotated[
        str, Field(min_length=5, max_length=20, description="Phone number")
    ]

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r"^\+\d{5,15}$", value):
            raise ValueError("Phone number must be entered in the format: +999999999")
        return value


class UpdateUserSchema(UserSchema):
    first_name: Annotated[
        Optional[str], Field(min_length=4, max_length=50, description="First name user")
    ] = None
    last_name: Annotated[
        Optional[str], Field(max_length=50, description="last name user")
    ] = None
    phone_number: Annotated[
        Optional[str], Field(min_length=5, max_length=20, description="Phone number")
    ] = None
    is_active: Optional[bool] = None


class ReadUserSchema(UserSchema):
    id: int
    is_active: bool
    created_at: datetime


class FilterParamsSchema(BaseSchema):
    status: Literal["is_active", "is_inactive", "all"] = "all"

    search: Annotated[
        Optional[str],
        Field(
            min_length=3,
            max_length=50,
            description="Search by keyword",
        ),
    ] = None

    date_from: Annotated[Optional[date], Field(description="start date")] = None
    date_to: Annotated[Optional[date], Field(description="end date")] = None

    sort_by: Annotated[
        Literal["created_at", "first_name", "last_name"], Field(description="sort by")
    ] = "created_at"
    sort_order: Annotated[Literal["asc", "desc"], Field(description="sort order")] = (
        "desc"
    )
