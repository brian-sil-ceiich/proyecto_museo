from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FeedbackCreate(BaseModel):
    id_peticion: int
    coincide_edad: int
    coincide_emocion: int


class FeedbackResponse(BaseModel):
    id: int
    # id_peticion: int
    # coincide_edad: int
    # coincide_emocion: int
    # fecha: datetime

    # model_config = ConfigDict(from_attributes=True)