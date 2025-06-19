from sqlmodel import SQLModel


class TokenPayload(BaseModel):
    sub: int | None = None

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
