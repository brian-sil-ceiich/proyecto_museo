from sqlalchemy.orm import Session

from app.models.feedback import Feedback

def crear_feedback(
    db: Session,
    id_peticion: str,
    coincide_edad: str,
    coincide_emocion: str 
    ) -> Feedback:

    print("Antes del try en db")
    try:
        feedback = Feedback(
            id_peticion=id_peticion,
            coincide_edad=coincide_edad,
            coincide_emocion=coincide_emocion
        )

        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        return feedback

    except Exception:
        db.rollback()
        raise