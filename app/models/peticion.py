from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Peticion(Base):
    __tablename__ = "peticion"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    folio: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    imagen: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    respuesta_ollama: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    feedback: Mapped[list["Feedback"]] = relationship(
        "Feedback",
        back_populates="peticion",
    )
