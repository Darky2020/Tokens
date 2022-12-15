from pydantic import BaseModel, Field
from ..constants import MAX_VALUE

class CreateArgs(BaseModel):
    ticker: str = Field(min_length=3, max_length=8)
    amount: int = Field(ge=1, le=MAX_VALUE)
    decimals: int = Field(ge=1, le=8)
    reissuable: bool

class TransferArgs(BaseModel):
    ticker: str = Field(min_length=3, max_length=8)
    amount: int = Field(ge=1, le=MAX_VALUE)

class IssueArgs(BaseModel):
    ticker: str = Field(min_length=3, max_length=8)
    amount: int = Field(ge=1, le=MAX_VALUE)
