from collections import defaultdict

from eth_typing import ChecksumAddress
from eth_utils.address import to_checksum_address

from python_sdk.common.constants import BASE_URL

JAM_SETTLEMENT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_permit2", "type": "address"},
            {"internalType": "address", "name": "_bebopBlend", "type": "address"},
            {"internalType": "address", "name": "_treasuryAddress", "type": "address"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {"inputs": [], "name": "AfterSettleHooksFailed", "type": "error"},
    {"inputs": [], "name": "BeforeSettleHooksFailed", "type": "error"},
    {"inputs": [], "name": "BuyTokensInvalidLength", "type": "error"},
    {"inputs": [], "name": "CallToBalanceManagerNotAllowed", "type": "error"},
    {"inputs": [], "name": "DifferentFeesInBatch", "type": "error"},
    {"inputs": [], "name": "DuplicateTokens", "type": "error"},
    {"inputs": [], "name": "FailedToSendEth", "type": "error"},
    {"inputs": [], "name": "InteractionsFailed", "type": "error"},
    {"inputs": [], "name": "InvalidBatchHooksLength", "type": "error"},
    {"inputs": [], "name": "InvalidBatchSignaturesLength", "type": "error"},
    {"inputs": [], "name": "InvalidBlendOrderType", "type": "error"},
    {"inputs": [], "name": "InvalidBlendPartnerId", "type": "error"},
    {"inputs": [], "name": "InvalidContractSignature", "type": "error"},
    {"inputs": [], "name": "InvalidExecutor", "type": "error"},
    {"inputs": [], "name": "InvalidFeePercentage", "type": "error"},
    {
        "inputs": [
            {"internalType": "uint256", "name": "expected", "type": "uint256"},
            {"internalType": "uint256", "name": "actual", "type": "uint256"},
        ],
        "name": "InvalidFilledAmounts",
        "type": "error",
    },
    {"inputs": [], "name": "InvalidFilledAmountsLength", "type": "error"},
    {"inputs": [], "name": "InvalidNonce", "type": "error"},
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "expected", "type": "uint256"},
            {"internalType": "uint256", "name": "actual", "type": "uint256"},
        ],
        "name": "InvalidOutputBalance",
        "type": "error",
    },
    {"inputs": [], "name": "InvalidPartnerAddress", "type": "error"},
    {"inputs": [], "name": "InvalidReceiverInBatch", "type": "error"},
    {"inputs": [], "name": "InvalidSignature", "type": "error"},
    {"inputs": [], "name": "InvalidSignatureLength", "type": "error"},
    {"inputs": [], "name": "InvalidSigner", "type": "error"},
    {"inputs": [], "name": "OrderExpired", "type": "error"},
    {"inputs": [], "name": "ReentrancyGuardReentrantCall", "type": "error"},
    {"inputs": [], "name": "SellTokensInvalidLength", "type": "error"},
    {"inputs": [], "name": "ZeroNonce", "type": "error"},
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint128", "name": "eventId", "type": "uint128"},
            {"indexed": True, "internalType": "address", "name": "receiver", "type": "address"},
            {"indexed": False, "internalType": "address[]", "name": "sellTokens", "type": "address[]"},
            {"indexed": False, "internalType": "address[]", "name": "buyTokens", "type": "address[]"},
            {"indexed": False, "internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
            {"indexed": False, "internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
        ],
        "name": "BebopBlendAggregateOrderFilled",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint128", "name": "eventId", "type": "uint128"},
            {"indexed": True, "internalType": "address", "name": "receiver", "type": "address"},
            {"indexed": False, "internalType": "address[]", "name": "sellTokens", "type": "address[]"},
            {"indexed": False, "internalType": "address[]", "name": "buyTokens", "type": "address[]"},
            {"indexed": False, "internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
            {"indexed": False, "internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
        ],
        "name": "BebopBlendMultiOrderFilled",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint128", "name": "eventId", "type": "uint128"},
            {"indexed": True, "internalType": "address", "name": "receiver", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "sellToken", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "buyToken", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "sellAmount", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "buyAmount", "type": "uint256"},
        ],
        "name": "BebopBlendSingleOrderFilled",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": False, "internalType": "address[]", "name": "sellTokens", "type": "address[]"},
            {"indexed": False, "internalType": "address[]", "name": "buyTokens", "type": "address[]"},
            {"indexed": False, "internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
            {"indexed": False, "internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
        ],
        "name": "BebopJamOrderFilled",
        "type": "event",
    },
    {"anonymous": False, "inputs": [], "name": "EIP712DomainChanged", "type": "event"},
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "receiver", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "NativeTransfer",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "DOMAIN_NAME",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "DOMAIN_SEPARATOR",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "DOMAIN_VERSION",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "EIP712_DOMAIN_TYPEHASH",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "balanceManager",
        "outputs": [{"internalType": "contract IJamBalanceManager", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "bebopBlend",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "nonce", "type": "uint256"}],
        "name": "cancelLimitOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "eip712Domain",
        "outputs": [
            {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "version", "type": "string"},
            {"internalType": "uint256", "name": "chainId", "type": "uint256"},
            {"internalType": "address", "name": "verifyingContract", "type": "address"},
            {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
            {"internalType": "uint256[]", "name": "extensions", "type": "uint256[]"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "components": [
                            {"internalType": "bool", "name": "result", "type": "bool"},
                            {"internalType": "address", "name": "to", "type": "address"},
                            {"internalType": "uint256", "name": "value", "type": "uint256"},
                            {"internalType": "bytes", "name": "data", "type": "bytes"},
                        ],
                        "internalType": "struct JamInteraction.Data[]",
                        "name": "beforeSettle",
                        "type": "tuple[]",
                    },
                    {
                        "components": [
                            {"internalType": "bool", "name": "result", "type": "bool"},
                            {"internalType": "address", "name": "to", "type": "address"},
                            {"internalType": "uint256", "name": "value", "type": "uint256"},
                            {"internalType": "bytes", "name": "data", "type": "bytes"},
                        ],
                        "internalType": "struct JamInteraction.Data[]",
                        "name": "afterSettle",
                        "type": "tuple[]",
                    },
                ],
                "internalType": "struct JamHooks.Def",
                "name": "hooks",
                "type": "tuple",
            }
        ],
        "name": "hashHooks",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "pure",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "taker", "type": "address"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint256", "name": "exclusivityDeadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint256", "name": "partnerInfo", "type": "uint256"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "bool", "name": "usingPermit2", "type": "bool"},
                ],
                "internalType": "struct JamOrder",
                "name": "order",
                "type": "tuple",
            },
            {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
        ],
        "name": "hashJamOrder",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "taker", "type": "address"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
        ],
        "name": "isLimitOrderNonceValid",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "taker", "type": "address"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint256", "name": "exclusivityDeadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint256", "name": "partnerInfo", "type": "uint256"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "bool", "name": "usingPermit2", "type": "bool"},
                ],
                "internalType": "struct JamOrder",
                "name": "order",
                "type": "tuple",
            },
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
            {
                "components": [
                    {"internalType": "bool", "name": "result", "type": "bool"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "internalType": "struct JamInteraction.Data[]",
                "name": "interactions",
                "type": "tuple[]",
            },
            {"internalType": "bytes", "name": "hooksData", "type": "bytes"},
            {"internalType": "address", "name": "balanceRecipient", "type": "address"},
        ],
        "name": "settle",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "taker", "type": "address"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint256", "name": "exclusivityDeadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint256", "name": "partnerInfo", "type": "uint256"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "bool", "name": "usingPermit2", "type": "bool"},
                ],
                "internalType": "struct JamOrder[]",
                "name": "orders",
                "type": "tuple[]",
            },
            {"internalType": "bytes[]", "name": "signatures", "type": "bytes[]"},
            {
                "components": [
                    {"internalType": "bool", "name": "result", "type": "bool"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "internalType": "struct JamInteraction.Data[]",
                "name": "interactions",
                "type": "tuple[]",
            },
            {
                "components": [
                    {
                        "components": [
                            {"internalType": "bool", "name": "result", "type": "bool"},
                            {"internalType": "address", "name": "to", "type": "address"},
                            {"internalType": "uint256", "name": "value", "type": "uint256"},
                            {"internalType": "bytes", "name": "data", "type": "bytes"},
                        ],
                        "internalType": "struct JamInteraction.Data[]",
                        "name": "beforeSettle",
                        "type": "tuple[]",
                    },
                    {
                        "components": [
                            {"internalType": "bool", "name": "result", "type": "bool"},
                            {"internalType": "address", "name": "to", "type": "address"},
                            {"internalType": "uint256", "name": "value", "type": "uint256"},
                            {"internalType": "bytes", "name": "data", "type": "bytes"},
                        ],
                        "internalType": "struct JamInteraction.Data[]",
                        "name": "afterSettle",
                        "type": "tuple[]",
                    },
                ],
                "internalType": "struct JamHooks.Def[]",
                "name": "hooks",
                "type": "tuple[]",
            },
            {"internalType": "address", "name": "balanceRecipient", "type": "address"},
        ],
        "name": "settleBatch",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "takerAddress", "type": "address"},
            {"internalType": "enum IBebopBlend.BlendOrderType", "name": "orderType", "type": "uint8"},
            {"internalType": "bytes", "name": "data", "type": "bytes"},
            {"internalType": "bytes", "name": "hooksData", "type": "bytes"},
        ],
        "name": "settleBebopBlend",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "taker", "type": "address"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint256", "name": "exclusivityDeadline", "type": "uint256"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint256", "name": "partnerInfo", "type": "uint256"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "bool", "name": "usingPermit2", "type": "bool"},
                ],
                "internalType": "struct JamOrder",
                "name": "order",
                "type": "tuple",
            },
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
            {"internalType": "uint256[]", "name": "filledAmounts", "type": "uint256[]"},
            {"internalType": "bytes", "name": "hooksData", "type": "bytes"},
        ],
        "name": "settleInternal",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "receiver", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transferNativeFromContract",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validationAddress", "type": "address"},
            {"internalType": "bytes32", "name": "hash", "type": "bytes32"},
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
        ],
        "name": "validateSignature",
        "outputs": [],
        "stateMutability": "view",
        "type": "function",
    },
    {"stateMutability": "payable", "type": "receive"},
]

HASH_HOOKS_ABI = {
    "inputs": [
        {
            "components": [
                {
                    "components": [
                        {"internalType": "bool", "name": "result", "type": "bool"},
                        {"internalType": "address", "name": "to", "type": "address"},
                        {"internalType": "uint256", "name": "value", "type": "uint256"},
                        {"internalType": "bytes", "name": "data", "type": "bytes"},
                    ],
                    "internalType": "struct JamInteraction.Data[]",
                    "name": "beforeSettle",
                    "type": "tuple[]",
                },
                {
                    "components": [
                        {"internalType": "bool", "name": "result", "type": "bool"},
                        {"internalType": "address", "name": "to", "type": "address"},
                        {"internalType": "uint256", "name": "value", "type": "uint256"},
                        {"internalType": "bytes", "name": "data", "type": "bytes"},
                    ],
                    "internalType": "struct JamInteraction.Data[]",
                    "name": "afterSettle",
                    "type": "tuple[]",
                },
            ],
            "internalType": "struct JamHooks.Def",
            "name": "hooks",
            "type": "tuple",
        }
    ],
    "name": "hashHooks",
    "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
    "stateMutability": "pure",
    "type": "function",
}


JAM_SETTLEMENT_CONTRACT: dict[int, ChecksumAddress] = defaultdict(
    lambda: to_checksum_address("0xbeb0b0623f66bE8cE162EbDfA2ec543A522F4ea6")
)
JAM_SETTLEMENT_CONTRACT[324] = to_checksum_address("0xB2Ef53BE5b9E7DF7754C3B9fa8218A6F7935389F")
JAM_BALANCE_MANAGER: dict[int, ChecksumAddress] = defaultdict(
    lambda: to_checksum_address("0xC5a350853E4e36b73EB0C24aaA4b8816C9A3579a")
)
JAM_BALANCE_MANAGER[324] = to_checksum_address("0xC4E18a890c2539a4367578006D695d39D3F15f85")

API_VERSION = 2
QUOTE_URL = BASE_URL + "/jam/{chain}/" + f"v{API_VERSION}/quote"
ORDER_URL = BASE_URL + "/jam/{chain}/" + f"v{API_VERSION}/order"
ORDER_STATUS_URL = BASE_URL + "/jam/{chain}/" + f"v{API_VERSION}/order-status"
