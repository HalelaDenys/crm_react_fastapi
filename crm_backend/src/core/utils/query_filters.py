from datetime import date
from typing import Optional

from core.utils.datetime_utils import make_utc_datetime
from sqlalchemy import or_
from sqlalchemy.sql import Select


def query_filters(
    stmt,
    model,
    status: str,
    search: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> Select:
    # Filtering by status
    if status == "is_active":
        stmt = stmt.where(model.is_active == True)
    elif status == "is_inactive":
        stmt = stmt.where(model.is_active == False)

    # Filtering by search
    if search:
        stmt = stmt.where(
            or_(
                model.first_name.ilike(f"%{search}%"),
                model.last_name.ilike(f"%{search}%"),
            )
        )

    # Filtering by creation date
    if date_from:
        date_from_dt = make_utc_datetime(date_from, end_of_day=True)
        stmt = stmt.where(model.created_at >= date_from_dt)

    if date_to:
        date_to_dt = make_utc_datetime(date_to, end_of_day=True)
        stmt = stmt.where(model.created_at <= date_to_dt)

    return stmt
