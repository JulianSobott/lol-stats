from pydantic import BaseModel


class ExceptionMessage(BaseModel):
    detail: str
