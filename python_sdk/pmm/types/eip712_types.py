from dataclasses import dataclass
from enum import Enum

from python_sdk.base_eip712_types import (
    EIP712Domain,
    EIP712DomainSeparatorSchema,
    EIP712Type,
    EIP712TypeSchema,
    StructuredEIP712Message,
)
from python_sdk.pmm.constants import PMM_SETTLEMENT_ADDRESS
from python_sdk.pmm.types.types import QuoteToSign


class OnchainOrderType(Enum):
    SingleOrder = "SingleOrder"
    MultiOrder = "MultiOrder"
    AggregateOrder = "AggregateOrder"


@dataclass
class PmmDomain(EIP712Domain):
    name: str = "BebopSettlement"
    version: str = "2"
    verifyingContract: str = PMM_SETTLEMENT_ADDRESS


class BaseSchema(EIP712TypeSchema):
    @classmethod
    def structured_message(cls, chain_id: int, message: QuoteToSign) -> StructuredEIP712Message:
        return StructuredEIP712Message(
            primaryType=cls.name,
            domain=PmmDomain(chainId=chain_id),
            types={
                EIP712DomainSeparatorSchema.name: EIP712DomainSeparatorSchema.types,
                cls.name: cls.types,
            },
            message=message,
        )


class SingleOrderSchema(BaseSchema):
    name: str = "SingleOrder"
    types: list[EIP712Type] = [
        EIP712Type(name="partner_id", type="uint64"),
        EIP712Type(name="expiry", type="uint256"),
        EIP712Type(name="taker_address", type="address"),
        EIP712Type(name="maker_address", type="address"),
        EIP712Type(name="maker_nonce", type="uint256"),
        EIP712Type(name="taker_token", type="address"),
        EIP712Type(name="maker_token", type="address"),
        EIP712Type(name="taker_amount", type="uint256"),
        EIP712Type(name="maker_amount", type="uint256"),
        EIP712Type(name="receiver", type="address"),
        EIP712Type(name="packed_commands", type="uint256"),
    ]


class MultiOrderSchema(BaseSchema):
    name: str = "MultiOrder"
    types: list[EIP712Type] = [
        EIP712Type(name="partner_id", type="uint64"),
        EIP712Type(name="expiry", type="uint256"),
        EIP712Type(name="taker_address", type="address"),
        EIP712Type(name="maker_address", type="address"),
        EIP712Type(name="maker_nonce", type="uint256"),
        EIP712Type(name="taker_tokens", type="address[]"),
        EIP712Type(name="maker_tokens", type="address[]"),
        EIP712Type(name="taker_amounts", type="uint256[]"),
        EIP712Type(name="maker_amounts", type="uint256[]"),
        EIP712Type(name="receiver", type="address"),
        EIP712Type(name="commands", type="bytes"),
    ]


class AggregateOrderSchema(BaseSchema):
    name: str = "AggregateOrder"
    types: list[EIP712Type] = [
        EIP712Type(name="partner_id", type="uint64"),
        EIP712Type(name="expiry", type="uint256"),
        EIP712Type(name="taker_address", type="address"),
        EIP712Type(name="maker_addresses", type="address[]"),
        EIP712Type(name="maker_nonces", type="uint256[]"),
        EIP712Type(name="taker_tokens", type="address[][]"),
        EIP712Type(name="maker_tokens", type="address[][]"),
        EIP712Type(name="taker_amounts", type="uint256[][]"),
        EIP712Type(name="maker_amounts", type="uint256[][]"),
        EIP712Type(name="receiver", type="address"),
        EIP712Type(name="commands", type="bytes"),
    ]


PmmSchemas = type[SingleOrderSchema] | type[MultiOrderSchema] | type[AggregateOrderSchema]

ORDER_TYPE_TO_SCHEMA: dict[OnchainOrderType, PmmSchemas] = {
    OnchainOrderType.SingleOrder: SingleOrderSchema,
    OnchainOrderType.MultiOrder: MultiOrderSchema,
    OnchainOrderType.AggregateOrder: AggregateOrderSchema,
}
