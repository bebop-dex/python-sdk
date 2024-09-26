from dataclasses import dataclass

from python_sdk.base_eip712_types import (
    EIP712Domain,
    EIP712DomainSeparatorSchema,
    EIP712Type,
    EIP712TypeSchema,
    StructuredEIP712Message,
)
from python_sdk.jam.constants import JAM_SETTLEMENT_ADDRESS
from python_sdk.jam.types.types import JamOrder


@dataclass
class JamDomain(EIP712Domain):
    name: str = "JamSettlement"
    version: str = "1"


class JamOrderSchema(EIP712TypeSchema):
    name: str = "JamOrder"
    types: list[EIP712Type] = [
        EIP712Type(name="taker", type="address"),
        EIP712Type(name="receiver", type="address"),
        EIP712Type(name="expiry", type="uint256"),
        EIP712Type(name="nonce", type="uint256"),
        EIP712Type(name="executor", type="address"),
        EIP712Type(name="minFillPercent", type="uint16"),
        EIP712Type(name="hooksHash", type="bytes32"),
        EIP712Type(name="sellTokens", type="address[]"),
        EIP712Type(name="buyTokens", type="address[]"),
        EIP712Type(name="sellAmounts", type="uint256[]"),
        EIP712Type(name="buyAmounts", type="uint256[]"),
        EIP712Type(name="sellNFTIds", type="uint256[]"),
        EIP712Type(name="buyNFTIds", type="uint256[]"),
        EIP712Type(name="sellTokenTransfers", type="bytes"),
        EIP712Type(name="buyTokenTransfers", type="bytes"),
    ]

    @classmethod
    def structured_message(cls, chain_id: int, message: JamOrder) -> StructuredEIP712Message:
        return StructuredEIP712Message(
            primaryType=cls.name,
            domain=JamDomain(chainId=chain_id, verifyingContract=JAM_SETTLEMENT_ADDRESS[chain_id]),
            types={
                EIP712DomainSeparatorSchema.name: EIP712DomainSeparatorSchema.types,
                cls.name: cls.types,
            },
            message=message,
        )
