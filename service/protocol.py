from pydantic import BaseModel, Field
from pydantic import ValidationError
from . import constants
import msgpack

MAX_VALUE = 10000000000000000000

class CategoryValidation(BaseModel):
    category: int = Field(ge=1, le=5)

class CreateValidation(CategoryValidation):
    ticker: str = Field(min_length=3, max_length=8)
    amount: int = Field(ge=1, le=MAX_VALUE)
    decimals: int = Field(ge=1, le=8)
    reissuable: bool

class IssueValidation(CategoryValidation):
    ticker: str = Field(min_length=3, max_length=8)
    amount: int = Field(ge=1, le=MAX_VALUE)

class TransferValidation(CategoryValidation):
    ticker: str = Field(min_length=3, max_length=8)
    amount: int = Field(ge=1, le=MAX_VALUE)

class Protocol(object):
    @classmethod
    def encode(cls, payload):
        # Validate category
        try:
            CategoryValidation(**payload)
        except ValidationError:
            return None

        category = payload["category"]

        # Validate the rest of the payload
        try:
            if category == constants.CREATE:
                data = CreateValidation(**payload)
                payload = {
                    "c": data.category,
                    "a": data.amount,
                    "t": data.ticker,
                    "r": data.reissuable
                }

            elif category == constants.ISSUE:
                data = IssueValidation(**payload)
                payload = {
                    "c": data.category,
                    "a": data.amount,
                    "t": data.ticker
                }

            elif category == constants.TRANSFER:
                data = TransferValidation(**payload)
                payload = {
                    "c": data.category,
                    "a": data.amount,
                    "t": data.ticker
                }

            elif category == constants.BAN:
                data = CategoryValidation(**payload)
                payload = {
                    "c": data.category
                }

            elif category == constants.UNBAN:
                data = CategoryValidation(**payload)
                payload = {
                    "c": data.category
                }

        except ValidationError as e:
            print("Failed to encode payload:", e)
            return None

        return msgpack.packb(payload).hex()

    @classmethod
    def decode(cls, data):
        # Validate bytes
        try:
            data = bytes.fromhex(data)
            payload = msgpack.unpackb(data)
        except ValueError:
            return None

        if "c" not in payload:
            return None

        payload["category"] = payload.pop("c")

        # Validate category
        try:
            CategoryValidation(**payload)
        except ValidationError:
            return None

        category = payload["category"]

        # Validate the rest of the payload
        try:
            if category == constants.CREATE:
                payload["amount"] = payload.pop("a")
                payload["ticker"] = payload.pop("t")
                payload["reissuable"] = payload.pop("r")

                CreateValidation(**payload)

            elif category == constants.ISSUE:
                payload["amount"] = payload.pop("a")
                payload["ticker"] = payload.pop("t")

                IssueValidation(**payload)

            elif category == constants.TRANSFER:
                payload["amount"] = payload.pop("a")
                payload["ticker"] = payload.pop("t")

                TransferValidation(**payload)

        except ValidationError as e:
            print("Failed to decode payload:", e)
            return None

        return payload
