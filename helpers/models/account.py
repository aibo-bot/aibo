from pydantic import BaseModel


class Account(BaseModel):
    user_id: int
    currency: int
    level: int
    exp: int
    max_exp: int
    description: str