from sqlmodel import SQLModel

class TokenPayload(SQLModel):
    sub: int | None = None

class Token(SQLModel):
    access_token: str
    token_type: str = 'bearer'
