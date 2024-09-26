from __future__ import annotations

from enum import Enum

from eth_typing import HexStr
from pydantic import BaseModel
from typing_extensions import TypedDict
from web3 import Web3


class ExpiryType(Enum):
    Standard = "standard"
    Short = "short"


class BaseOrderToSign(BaseModel):
    partner_id: int
    expiry: int
    taker_address: str
    receiver: str


class BaseOrder(TypedDict):
    partner_id: int
    expiry: int
    taker_address: str
    receiver: str


class SingleOrderToSign(BaseOrderToSign):
    maker_address: str
    maker_nonce: str
    taker_token: str
    maker_token: str
    taker_amount: str
    maker_amount: str
    packed_commands: str

    @property
    def signable_message(self) -> SingleOrder:
        return SingleOrder(
            partner_id=self.partner_id,
            expiry=self.expiry,
            taker_address=self.taker_address,
            maker_address=self.maker_address,
            maker_nonce=int(self.maker_nonce),
            taker_token=self.taker_token,
            maker_token=self.maker_token,
            taker_amount=int(self.taker_amount),
            maker_amount=int(self.maker_amount),
            receiver=self.receiver,
            packed_commands=int(self.packed_commands),
        )


class SingleOrder(BaseOrder):
    maker_address: str
    maker_nonce: int
    taker_token: str
    maker_token: str
    taker_amount: int
    maker_amount: int
    packed_commands: int


class MultiOrderToSign(BaseOrderToSign):
    maker_address: str
    maker_nonce: str
    taker_tokens: list[str]
    maker_tokens: list[str]
    taker_amounts: list[str]
    maker_amounts: list[str]
    commands: str

    @property
    def signable_message(self) -> MultiOrder:
        return MultiOrder(
            partner_id=self.partner_id,
            expiry=self.expiry,
            taker_address=self.taker_address,
            maker_address=self.maker_address,
            maker_nonce=int(self.maker_nonce),
            taker_tokens=self.taker_tokens,
            maker_tokens=self.maker_tokens,
            taker_amounts=[int(amt) for amt in self.taker_amounts],
            maker_amounts=[int(amt) for amt in self.maker_amounts],
            receiver=self.receiver,
            commands=Web3.to_bytes(hexstr=HexStr(self.commands)),
        )


class MultiOrder(BaseOrder):
    maker_address: str
    maker_nonce: int
    taker_tokens: list[str]
    maker_tokens: list[str]
    taker_amounts: list[int]
    maker_amounts: list[int]
    commands: bytes


class AggregateOrderToSign(BaseOrderToSign):
    maker_addresses: list[str]
    maker_nonces: list[str]
    taker_tokens: list[list[str]]
    maker_tokens: list[list[str]]
    taker_amounts: list[list[str]]
    maker_amounts: list[list[str]]
    commands: str

    @property
    def signable_message(self) -> AggregateOrder:
        return AggregateOrder(
            partner_id=self.partner_id,
            expiry=self.expiry,
            taker_address=self.taker_address,
            receiver=self.receiver,
            maker_addresses=self.maker_addresses,
            maker_nonces=[int(nonce) for nonce in self.maker_nonces],
            taker_tokens=self.taker_tokens,
            maker_tokens=self.maker_tokens,
            taker_amounts=[[int(amt) for amt in amounts] for amounts in self.taker_amounts],
            maker_amounts=[[int(amt) for amt in amounts] for amounts in self.maker_amounts],
            commands=Web3.to_bytes(hexstr=HexStr(self.commands)),
        )


class AggregateOrder(BaseOrder):
    maker_addresses: list[str]
    maker_nonces: list[int]
    taker_tokens: list[list[str]]
    maker_tokens: list[list[str]]
    taker_amounts: list[list[int]]
    maker_amounts: list[list[int]]
    commands: bytes


QuoteToSignApiResponse = SingleOrderToSign | MultiOrderToSign | AggregateOrderToSign
QuoteToSign = SingleOrder | MultiOrder | AggregateOrder
