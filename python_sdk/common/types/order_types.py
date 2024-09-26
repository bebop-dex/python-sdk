from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel


# ---------------------------------------------------------------------------- #
#                                 Request Types                                #
# ---------------------------------------------------------------------------- #
@dataclass(init=True, frozen=True, order=True)
class Permit:
    signature: str
    approvals_deadline: int


@dataclass(init=True, frozen=True, order=True)
class Permit2:
    signature: str
    approvals_deadline: int
    token_addresses: list[str]
    token_nonces: list[int]


class OrderRequest(BaseModel):
    quote_id: str
    signature: str
    sign_scheme: str = "EIP712"
    permit2: Permit2 | None = None
    permit: Permit | None = None


class OrderStatusRequest(BaseModel):
    quote_id: str


# ---------------------------------------------------------------------------- #
#                                Response Types                                #
# ---------------------------------------------------------------------------- #
class OrderApiStatus(StrEnum):
    Pending = "Pending"
    Success = "Success"
    Settled = "Settled"
    Confirmed = "Confirmed"
    Failed = "Failed"


class OrderResponse(BaseModel):
    status: str
    expiry: int
    txHash: str | None = None


class OrderStatusResponse(BaseModel):
    status: OrderApiStatus
    txHash: str | None = None
    amounts: dict[str, str] | None = None
