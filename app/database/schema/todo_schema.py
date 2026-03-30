from sqlalchemy import Column, Integer, String, Boolean, VARCHAR, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from ..db import Base


class TodoSchema(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
