from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

# Example of message object: https://github.com/ethereum/eth-account/blob/master/tests/fixtures/valid_eip712_example_with_array.json


@dataclass
class EIP712Domain:
    chainId: int
    verifyingContract: str
    name: str
    version: str


@dataclass
class EIP712Type(ABC):
    name: str
    type: str


@dataclass
class StructuredEIP712Message(ABC):
    primaryType: str
    domain: EIP712Domain
    types: dict[str, list[EIP712Type]]
    message: Any


@dataclass
class EIP712TypeSchema(ABC):
    name: str
    types: list[EIP712Type]

    @classmethod
    @abstractmethod
    def structured_message(cls, chain_id: int, message: Any) -> StructuredEIP712Message: ...


class EIP712DomainSeparatorSchema(EIP712TypeSchema):
    name: str = "EIP712Domain"
    types: list[EIP712Type] = [
        EIP712Type(name="name", type="string"),
        EIP712Type(name="version", type="string"),
        EIP712Type(name="chainId", type="uint256"),
        EIP712Type(name="verifyingContract", type="address"),
    ]
