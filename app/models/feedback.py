from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_peticion: Mapped[int] = mapped_column(
        ForeignKey("peticion.id"),
        nullable=False,
    )

    coincide_edad: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    coincide_emocion: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    peticion: Mapped["Peticion"] = relationship(
        "Peticion",
        back_populates="feedback",
    )
