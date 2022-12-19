from pydantic import BaseModel, Field
from typing import Union
from .. import constants

class BuildArgs(BaseModel):
    receive_address: Union[str, None] = Field(default=None)
    marker: float = Field(default=constants.DEFAULT_MARKER)
    fee: float = Field(default=constants.DEFAULT_FEE)
    send_address: str
    payload: str