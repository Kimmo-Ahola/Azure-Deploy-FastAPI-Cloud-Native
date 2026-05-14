# Databasmodell, detta sparas till sqlite

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # detta är en ORM-funktion för att vi ska kunna skriva joins enklare
    tasks: Mapped[list["Task"]] = relationship(back_populates="category")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(default=None)
    done: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())



    """
    Nya kolumner för att få relationer mellan tasks
    """
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.category_id"), default=None
    )

    category: Mapped[Optional["Category"]] = relationship(back_populates="tasks")
