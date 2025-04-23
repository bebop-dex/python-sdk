from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import TypedDict


class JamOrderToSign(BaseModel):
    taker: str
    receiver: str
    expiry: int
    exclusivityDeadline: int
    nonce: str
    executor: str
    partnerInfo: int
    sellTokens: list[str]
    buyTokens: list[str]
    sellAmounts: list[str]
    buyAmounts: list[str]
    hooksHash: str

    @property
    def signable_message(self) -> JamOrder:
        return JamOrder(
            taker=self.taker,
            receiver=self.receiver,
            expiry=self.expiry,
            exclusivityDeadline=self.exclusivityDeadline,
            nonce=int(self.nonce),
            executor=self.executor,
            partnerInfo=self.partnerInfo,
            hooksHash=self.hooksHash,
            sellTokens=self.sellTokens,
            buyTokens=self.buyTokens,
            sellAmounts=list(map(int, (self.sellAmounts))),
            buyAmounts=list(map(int, (self.buyAmounts))),
        )


class JamOrder(TypedDict):
    taker: str
    receiver: str
    expiry: int
    exclusivityDeadline: int
    nonce: int
    executor: str
    partnerInfo: int
    sellTokens: list[str]
    buyTokens: list[str]
    sellAmounts: list[int]
    buyAmounts: list[int]
    hooksHash: str
