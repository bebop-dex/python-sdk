import asyncio
import os

from dotenv import load_dotenv
from eth_typing import HexStr

from python_sdk.common.types.order_types import OrderStatusResponse
from python_sdk.common.types.types import Chain, Env
from python_sdk.pmm.client import PMMClient
from python_sdk.pmm.types.quote_types import QuoteRequest, QuoteResponse

# Arbitrum Tokens
WETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
USDC = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
USDT = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"

load_dotenv()

private_key: str | None = os.getenv("PRIVATE_KEY")
assert private_key
pmm_client = PMMClient(env=Env.TEST, chain=Chain.arbitrum, private_key=private_key)


async def quote_example() -> QuoteResponse:
    quote_request = QuoteRequest(sell_tokens=[USDT], buy_tokens=[WETH], sell_amounts=[2_000_000])
    return await pmm_client.get_quote(quote_request)


async def gasless_order_example() -> OrderStatusResponse:
    quote_request = QuoteRequest(sell_tokens=[USDT], buy_tokens=[WETH], sell_amounts=[2_000_000])
    return await pmm_client.send_gasless_order(quote_request)


async def taker_order_example() -> tuple[HexStr, bool]:
    quote_request = QuoteRequest(sell_tokens=[WETH], buy_tokens=[USDT], sell_amounts=[int(1e15)], gasless=False)
    return await pmm_client.send_taker_order(quote_request)


async def approve_pmm_tokens() -> None:
    await pmm_client.approve_token(USDT, 2**256 - 1)
    await pmm_client.approve_token(WETH, 2**256 - 1)
    await pmm_client.approve_token(USDC, 2**256 - 1)


if __name__ == "__main__":
    asyncio.run(taker_order_example())
