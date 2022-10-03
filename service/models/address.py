from sqlmodel import Field, Relationship
from .base import BaseTable
from typing import Optional
from typing import List

class Address(BaseTable, table=True):
    __tablename__ = "service_addresses"

    address: str
    nonce: int

    balances: List["Balance"] = Relationship(back_populates="address")

    transfers_send: List["Transfer"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs=dict(
            primaryjoin="Address.id==Transfer.sender_id"
        )
    )

    transfers_receive: List["Transfer"] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs=dict(
            primaryjoin="Address.id==Transfer.receiver_id"
        )
    )