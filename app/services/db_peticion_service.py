from sqlalchemy.orm import Session

from app.models.peticion import Peticion

def crear_peticion(
    db: Session,
    folio: str,
    imagen: str,
    respuesta_ollama: str | None = None
    ) -> Peticion:

    try:
        peticion = Peticion(
            folio=folio,
            imagen=imagen,
            respuesta_ollama=respuesta_ollama
        )

        db.add(peticion)
        db.commit()
        db.refresh(peticion)

        return peticion

    except Exception:
        db.rollback()
        raise

def actualizar_respuesta_ollama(
    db: Session,
    id_peticion: int,
    respuesta_ollama: str
    ) -> Peticion:

    try:
        peticion = db.get(Peticion, id_peticion)

        if peticion is None:
            raise ValueError(
                f"No existe la petición con ID {id_peticion}"
            )

        peticion.respuesta_ollama = respuesta_ollama

        db.commit()
        db.refresh(peticion)

        return peticion

    except Exception:
        db.rollback()
        raise