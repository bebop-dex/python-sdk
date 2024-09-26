from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import TypedDict


class JamOrderToSign(BaseModel):
    taker: str
    receiver: str
    expiry: int
    nonce: str
    executor: str
    minFillPercent: int
    hooksHash: str
    sellTokens: list[str]
    buyTokens: list[str]
    sellAmounts: list[str]
    buyAmounts: list[str]
    sellNFTIds: list[str]
    buyNFTIds: list[str]
    sellTokenTransfers: str
    buyTokenTransfers: str

    @property
    def signable_message(self) -> JamOrder:
        return JamOrder(
            taker=self.taker,
            receiver=self.receiver,
            expiry=self.expiry,
            nonce=int(self.nonce),
            executor=self.executor,
            minFillPercent=self.minFillPercent,
            hooksHash=self.hooksHash,
            sellTokens=self.sellTokens,
            buyTokens=self.buyTokens,
            sellAmounts=list(map(int, (self.sellAmounts))),
            buyAmounts=list(map(int, (self.buyAmounts))),
            sellNFTIds=self.sellNFTIds,
            buyNFTIds=self.buyNFTIds,
            sellTokenTransfers=self.sellTokenTransfers,
            buyTokenTransfers=self.buyTokenTransfers,
        )


class JamOrder(TypedDict):
    taker: str
    receiver: str
    expiry: int
    nonce: int
    executor: str
    minFillPercent: int
    hooksHash: str
    sellTokens: list[str]
    buyTokens: list[str]
    sellAmounts: list[int]
    buyAmounts: list[int]
    sellNFTIds: list[str]
    buyNFTIds: list[str]
    sellTokenTransfers: str
    buyTokenTransfers: str
