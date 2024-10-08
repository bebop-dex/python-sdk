from collections import defaultdict

from eth_typing import ChecksumAddress
from eth_utils.address import to_checksum_address

from python_sdk.common.constants import BASE_URL
from python_sdk.common.types.types import Chain

JAM_SETTLEMENT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_permit2", "type": "address"},
            {"internalType": "address", "name": "_daiAddress", "type": "address"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
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
        "anonymous": False,
        "inputs": [{"indexed": True, "internalType": "uint256", "name": "nonce", "type": "uint256"}],
        "name": "Settlement",
        "type": "event",
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
        "name": "EIP712_DOMAIN_TYPEHASH",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "JAM_ORDER_TYPE_HASH",
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
        "inputs": [{"internalType": "uint256", "name": "nonce", "type": "uint256"}],
        "name": "cancelLimitOrder",
        "outputs": [],
        "stateMutability": "nonpayable",
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
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint16", "name": "minFillPercent", "type": "uint16"},
                    {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "sellNFTIds", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyNFTIds", "type": "uint256[]"},
                    {"internalType": "bytes", "name": "sellTokenTransfers", "type": "bytes"},
                    {"internalType": "bytes", "name": "buyTokenTransfers", "type": "bytes"},
                ],
                "internalType": "struct JamOrder.Data",
                "name": "order",
                "type": "tuple",
            },
            {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
        ],
        "name": "hashOrder",
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
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256[]", "name": "", "type": "uint256[]"},
            {"internalType": "uint256[]", "name": "", "type": "uint256[]"},
            {"internalType": "bytes", "name": "", "type": "bytes"},
        ],
        "name": "onERC1155BatchReceived",
        "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "bytes", "name": "", "type": "bytes"},
        ],
        "name": "onERC1155Received",
        "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "address", "name": "", "type": "address"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "bytes", "name": "", "type": "bytes"},
        ],
        "name": "onERC721Received",
        "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "taker", "type": "address"},
                    {"internalType": "address", "name": "receiver", "type": "address"},
                    {"internalType": "uint256", "name": "expiry", "type": "uint256"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint16", "name": "minFillPercent", "type": "uint16"},
                    {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "sellNFTIds", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyNFTIds", "type": "uint256[]"},
                    {"internalType": "bytes", "name": "sellTokenTransfers", "type": "bytes"},
                    {"internalType": "bytes", "name": "buyTokenTransfers", "type": "bytes"},
                ],
                "internalType": "struct JamOrder.Data",
                "name": "order",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "enum Signature.Type", "name": "signatureType", "type": "uint8"},
                    {"internalType": "bytes", "name": "signatureBytes", "type": "bytes"},
                ],
                "internalType": "struct Signature.TypedSignature",
                "name": "signature",
                "type": "tuple",
            },
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
                "internalType": "struct JamHooks.Def",
                "name": "hooks",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "address", "name": "balanceRecipient", "type": "address"},
                    {"internalType": "uint16", "name": "curFillPercent", "type": "uint16"},
                ],
                "internalType": "struct ExecInfo.SolverData",
                "name": "solverData",
                "type": "tuple",
            },
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
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint16", "name": "minFillPercent", "type": "uint16"},
                    {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "sellNFTIds", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyNFTIds", "type": "uint256[]"},
                    {"internalType": "bytes", "name": "sellTokenTransfers", "type": "bytes"},
                    {"internalType": "bytes", "name": "buyTokenTransfers", "type": "bytes"},
                ],
                "internalType": "struct JamOrder.Data[]",
                "name": "orders",
                "type": "tuple[]",
            },
            {
                "components": [
                    {"internalType": "enum Signature.Type", "name": "signatureType", "type": "uint8"},
                    {"internalType": "bytes", "name": "signatureBytes", "type": "bytes"},
                ],
                "internalType": "struct Signature.TypedSignature[]",
                "name": "signatures",
                "type": "tuple[]",
            },
            {
                "components": [
                    {"internalType": "bytes[]", "name": "permitSignatures", "type": "bytes[]"},
                    {"internalType": "bytes", "name": "signatureBytesPermit2", "type": "bytes"},
                    {"internalType": "uint48[]", "name": "noncesPermit2", "type": "uint48[]"},
                    {"internalType": "uint48", "name": "deadline", "type": "uint48"},
                ],
                "internalType": "struct Signature.TakerPermitsInfo[]",
                "name": "takersPermitsInfo",
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
            {
                "components": [
                    {"internalType": "address", "name": "balanceRecipient", "type": "address"},
                    {"internalType": "uint16[]", "name": "curFillPercents", "type": "uint16[]"},
                    {"internalType": "bool[]", "name": "takersPermitsUsage", "type": "bool[]"},
                    {"internalType": "bool", "name": "transferExactAmounts", "type": "bool"},
                ],
                "internalType": "struct ExecInfo.BatchSolverData",
                "name": "solverData",
                "type": "tuple",
            },
        ],
        "name": "settleBatch",
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
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint16", "name": "minFillPercent", "type": "uint16"},
                    {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "sellNFTIds", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyNFTIds", "type": "uint256[]"},
                    {"internalType": "bytes", "name": "sellTokenTransfers", "type": "bytes"},
                    {"internalType": "bytes", "name": "buyTokenTransfers", "type": "bytes"},
                ],
                "internalType": "struct JamOrder.Data",
                "name": "order",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "enum Signature.Type", "name": "signatureType", "type": "uint8"},
                    {"internalType": "bytes", "name": "signatureBytes", "type": "bytes"},
                ],
                "internalType": "struct Signature.TypedSignature",
                "name": "signature",
                "type": "tuple",
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
                "internalType": "struct JamHooks.Def",
                "name": "hooks",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "uint256[]", "name": "increasedBuyAmounts", "type": "uint256[]"},
                    {"internalType": "uint16", "name": "curFillPercent", "type": "uint16"},
                ],
                "internalType": "struct ExecInfo.MakerData",
                "name": "makerData",
                "type": "tuple",
            },
        ],
        "name": "settleInternal",
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
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint16", "name": "minFillPercent", "type": "uint16"},
                    {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "sellNFTIds", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyNFTIds", "type": "uint256[]"},
                    {"internalType": "bytes", "name": "sellTokenTransfers", "type": "bytes"},
                    {"internalType": "bytes", "name": "buyTokenTransfers", "type": "bytes"},
                ],
                "internalType": "struct JamOrder.Data",
                "name": "order",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "enum Signature.Type", "name": "signatureType", "type": "uint8"},
                    {"internalType": "bytes", "name": "signatureBytes", "type": "bytes"},
                ],
                "internalType": "struct Signature.TypedSignature",
                "name": "signature",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "bytes[]", "name": "permitSignatures", "type": "bytes[]"},
                    {"internalType": "bytes", "name": "signatureBytesPermit2", "type": "bytes"},
                    {"internalType": "uint48[]", "name": "noncesPermit2", "type": "uint48[]"},
                    {"internalType": "uint48", "name": "deadline", "type": "uint48"},
                ],
                "internalType": "struct Signature.TakerPermitsInfo",
                "name": "takerPermitsInfo",
                "type": "tuple",
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
                "internalType": "struct JamHooks.Def",
                "name": "hooks",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "uint256[]", "name": "increasedBuyAmounts", "type": "uint256[]"},
                    {"internalType": "uint16", "name": "curFillPercent", "type": "uint16"},
                ],
                "internalType": "struct ExecInfo.MakerData",
                "name": "makerData",
                "type": "tuple",
            },
        ],
        "name": "settleInternalWithPermitsSignatures",
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
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "address", "name": "executor", "type": "address"},
                    {"internalType": "uint16", "name": "minFillPercent", "type": "uint16"},
                    {"internalType": "bytes32", "name": "hooksHash", "type": "bytes32"},
                    {"internalType": "address[]", "name": "sellTokens", "type": "address[]"},
                    {"internalType": "address[]", "name": "buyTokens", "type": "address[]"},
                    {"internalType": "uint256[]", "name": "sellAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyAmounts", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "sellNFTIds", "type": "uint256[]"},
                    {"internalType": "uint256[]", "name": "buyNFTIds", "type": "uint256[]"},
                    {"internalType": "bytes", "name": "sellTokenTransfers", "type": "bytes"},
                    {"internalType": "bytes", "name": "buyTokenTransfers", "type": "bytes"},
                ],
                "internalType": "struct JamOrder.Data",
                "name": "order",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "enum Signature.Type", "name": "signatureType", "type": "uint8"},
                    {"internalType": "bytes", "name": "signatureBytes", "type": "bytes"},
                ],
                "internalType": "struct Signature.TypedSignature",
                "name": "signature",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "bytes[]", "name": "permitSignatures", "type": "bytes[]"},
                    {"internalType": "bytes", "name": "signatureBytesPermit2", "type": "bytes"},
                    {"internalType": "uint48[]", "name": "noncesPermit2", "type": "uint48[]"},
                    {"internalType": "uint48", "name": "deadline", "type": "uint48"},
                ],
                "internalType": "struct Signature.TakerPermitsInfo",
                "name": "takerPermitsInfo",
                "type": "tuple",
            },
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
                "internalType": "struct JamHooks.Def",
                "name": "hooks",
                "type": "tuple",
            },
            {
                "components": [
                    {"internalType": "address", "name": "balanceRecipient", "type": "address"},
                    {"internalType": "uint16", "name": "curFillPercent", "type": "uint16"},
                ],
                "internalType": "struct ExecInfo.SolverData",
                "name": "solverData",
                "type": "tuple",
            },
        ],
        "name": "settleWithPermitsSignatures",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}],
        "name": "supportsInterface",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
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
            {
                "components": [
                    {"internalType": "enum Signature.Type", "name": "signatureType", "type": "uint8"},
                    {"internalType": "bytes", "name": "signatureBytes", "type": "bytes"},
                ],
                "internalType": "struct Signature.TypedSignature",
                "name": "signature",
                "type": "tuple",
            },
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


JAM_SETTLEMENT_ADDRESS: dict[int, ChecksumAddress] = defaultdict(
    lambda: to_checksum_address("0xbEbEbEb035351f58602E0C1C8B59ECBfF5d5f47b")
)
JAM_SETTLEMENT_ADDRESS[324] = to_checksum_address("0x574d1fcF950eb48b11de5DF22A007703cbD2b129")
JAM_BALANCE_MANAGER: dict[int, ChecksumAddress] = defaultdict(
    lambda: to_checksum_address("0xfE96910cF84318d1B8a5e2a6962774711467C0be")
)
JAM_BALANCE_MANAGER[324] = to_checksum_address("0x10D7a281c39713B34751Fcc0830ea2AE56D64B2C")

SUPPORTED_CHAINS = {Chain.ethereum, Chain.polygon, Chain.arbitrum, Chain.blast, Chain.optimism, Chain.blast}

API_VERSION = 1
QUOTE_URL = BASE_URL + "/jam/{chain}/" + f"v{API_VERSION}/quote"
ORDER_URL = BASE_URL + "/jam/{chain}/" + f"v{API_VERSION}/order"
ORDER_STATUS_URL = BASE_URL + "/jam/{chain}/" + f"v{API_VERSION}/order-status"
