from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum, IntEnum
from typing import Any

from python_sdk.common.constants import NATIVE_TOKEN


class Env(Enum):
    PROD = "PROD"
    TEST = "TEST"


class Route(Enum):
    JAM = "JAM"
    PMM = "PMM"


class ApprovalType(str, Enum):
    Standard = "Standard"
    Permit = "Permit"
    Permit2 = "Permit2"


@dataclass
class ChainInfo:
    native_name: str
    native_symbol: str
    wrapped_address: str
    wrapped_symbol: str
    explorer: str
    tokens: dict[str, str]
    public_rpc: str
    permit2_address: str = "0x000000000022D473030F116dDEE9F6B43aC78BA3"
    multicall_address: str = "0xcA11bde05977b3631167028862bE2a173976CA11"
    arbitrum_like: bool = False
    optimism_like: bool = False


class Chain(IntEnum):
    ethereum = (
        1,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            wrapped_symbol="WETH",
            explorer="https://etherscan.io",
            public_rpc="https://eth.drpc.org",
            tokens={
                "1INCH": "0x111111111117dC0aa78b770fA6A738034120C302",
                "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",
                "APE": "0x4d224452801ACEd8B2F0aebE155379bb5D594381",
                "BAL": "0xba100000625a3754423978a60c9317c58a424e3D",
                "BAT": "0x0D8775F648430679A709E98d2b0Cb6250d2887EF",
                "BUSD": "0x4Fabb145d64652a948d72533023f6E7A623C7C53",
                "COMP": "0xc00e94Cb662C3520282E6f5717214004A7f26888",
                "CRV": "0xD533a949740bb3306d119CC777fa900bA034cd52",
                "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "FTM": "0x4E15361FD6b4BB609Fa63C81A2be19d873717870",
                "GALA": "0x15D4c048F83bd7e37d49eA4C83a07267Ec4203dA",
                "GRT": "0xc944E90C64B2c07662A292be6244BDf05Cda44a7",
                "IMX": "0xF57e7e7C23978C3cAEC3C3548E3D615c346e79fF",
                "LDO": "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",
                "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
                "MATIC": "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
                "MKR": "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2",
                "MPL": "0x33349B282065b0284d756F0577FB39c158F935e6",
                "MULTI": "0x65Ef703f5594D2573eb71Aaf55BC0CB548492df4",
                "PAX": "0x8E870D67F660D95d5be530380D0eC0bd388289E1",
                "SAND": "0x3845badAde8e6dFF049820680d1F14bD3903a5d0",
                "SHIB": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
                "SUSHI": "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2",
                "TUSD": "0x0000000000085d4780B73119b644AE5ecd22b376",
                "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
                "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "YFI": "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",
                "ZRX": "0xE41d2489571d322189246DaFA5ebDe1F4699F498",
            },
        ),
    )
    polygon = (
        137,
        ChainInfo(
            native_name="Matic",
            native_symbol="MATIC",
            wrapped_address="0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
            wrapped_symbol="WMATIC",
            explorer="https://polygonscan.com",
            public_rpc="https://polygon.drpc.org",
            tokens={
                "AAVE": "0xD6DF932A45C0f255f85145f286eA0b292B21C90B",
                "BAL": "0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3",
                "CRV": "0x172370d5Cd63279eFa6d502DAB29171933a610AF",
                "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
                "LINK": "0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39",
                "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
                "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
                "WBTC": "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6",
                "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
                "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
            },
        ),
    )
    arbitrum = (
        42161,
        ChainInfo(
            native_name="Arbitrum ETH",
            native_symbol="ETH",
            wrapped_address="0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
            wrapped_symbol="WETH",
            arbitrum_like=True,
            explorer="https://arbiscan.io",
            public_rpc="https://arbitrum.drpc.org",
            tokens={
                "RDNT": "0x3082CC23568eA640225c2467653dB90e9250AaA0",
                "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
                "ARB": "0x912CE59144191C1204E64559FE8253a0e49E6548",
                "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
                "GMX": "0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a",
                "MAGIC": "0x539bdE0d7Dbd336b79148AA742883198BBF60342",
                "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
                "ETH": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
                "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
                "WBTC": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
            },
        ),
    )

    bsc = (
        56,
        ChainInfo(
            native_name="BNB",
            native_symbol="BNB",
            wrapped_address="0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
            wrapped_symbol="WBNB",
            explorer="https://bscscan.com",
            public_rpc="https://bsc.drpc.org",
            tokens={},
        ),
    )

    zksync = (
        324,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
            wrapped_symbol="WETH",
            permit2_address="0x0000000000225e31D15943971F47aD3022F714Fa",
            multicall_address="0xF9cda624FBC7e059355ce98a31693d299FACd963",
            explorer="https://era.zksync.network",
            public_rpc="https://zksync.drpc.org",
            tokens={},
        ),
    )

    optimism = (
        10,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0x4200000000000000000000000000000000000006",
            wrapped_symbol="WETH",
            multicall_address="0xcA11bde05977b3631167028862bE2a173976CA11",
            optimism_like=True,
            explorer="https://optimistic.etherscan.io",
            public_rpc="https://mainnet.optimism.io",
            tokens={
                "WETH": "0x4200000000000000000000000000000000000006",
                "USDC": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
                "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
                "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
                "WBTC": "0x68f180fcCe6836688e9084f035309E29Bf0A2095",
            },
        ),
    )

    blast = (
        81457,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0x4300000000000000000000000000000000000004",
            wrapped_symbol="WETH",
            multicall_address="0xcA11bde05977b3631167028862bE2a173976CA11",
            optimism_like=True,
            explorer="https://blastscan.io",
            public_rpc="https://blast.drpc.org/",
            tokens={},
        ),
    )

    base = (
        8453,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0x4200000000000000000000000000000000000006",
            wrapped_symbol="WETH",
            multicall_address="0xcA11bde05977b3631167028862bE2a173976CA11",
            optimism_like=True,
            explorer="https://basescan.org",
            public_rpc="https://base.drpc.org",
            tokens={},
        ),
    )

    mode = (
        34443,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0x4200000000000000000000000000000000000006",
            wrapped_symbol="WETH",
            multicall_address="0xcA11bde05977b3631167028862bE2a173976CA11",
            optimism_like=True,
            explorer="https://explorer.mode.network",
            public_rpc="https://mode.drpc.org/",
            tokens={},
        ),
    )

    scroll = (
        534352,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0x5300000000000000000000000000000000000004",
            wrapped_symbol="WETH",
            multicall_address="0xcA11bde05977b3631167028862bE2a173976CA11",
            optimism_like=True,
            explorer="https://scrollscan.com",
            public_rpc="https://scroll.drpc.org",
            tokens={},
        ),
    )

    taiko = (
        167000,
        ChainInfo(
            native_name="Ethereum",
            native_symbol="ETH",
            wrapped_address="0xA51894664A773981C6C112C43ce576f315d5b1B6",
            wrapped_symbol="WETH",
            multicall_address="0xcA11bde05977b3631167028862bE2a173976CA11",  # Needs to be deployed
            optimism_like=False,
            explorer="https://taikoscan.io",
            public_rpc="https://rpc.mainnet.taiko.xyz",
            tokens={},
        ),
    )

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.id: int
        self.native_name: str
        self.native_symbol: str
        self.wrapped_address: str
        self.wrapped_symbol: str
        self.permit2_address: str
        self.multicall_address: str
        self.arbitrum_like: bool
        self.optimism_like: bool
        self.explorer: str
        self.tokens: dict[str, str]
        self.emoji: str
        self.public_rpc: str

    def __new__(cls, value: int, info: ChainInfo) -> Chain:
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.id = value
        for kev, value in asdict(info).items():
            setattr(obj, kev, value)
        return obj

    @property
    def display_name(self) -> str:
        return self.name.capitalize()

    def wrap_if_native(self, address: str) -> str:
        if address != NATIVE_TOKEN:
            return address
        return self.wrapped_address

    def tx_link(self, tx_hash: str) -> str:
        return f"{self.explorer}/tx/{tx_hash}"

    def address_link(self, address: str) -> str:
        return f"{self.explorer}/address/{address}"
