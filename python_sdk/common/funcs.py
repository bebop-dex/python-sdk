import asyncio
from typing import Any

import aiohttp
from eth_account.signers.local import LocalAccount
from eth_typing import HexStr
from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.exceptions import TransactionNotFound

from python_sdk.common.constants import ERROR_KEY
from python_sdk.common.types.order_types import OrderRequest, OrderResponse, OrderStatusRequest, OrderStatusResponse
from python_sdk.common.types.types import Chain, Env
from python_sdk.common.utils.logger import Logger
from python_sdk.jam.types.quote_types import QuoteResponse as JamQuoteResponse
from python_sdk.pmm.types.quote_types import QuoteResponse as PmmQuoteResponse

LOGGER = Logger(__name__)


async def send_taker_order(
    chain: Chain, web3: AsyncWeb3, account: LocalAccount, quote: PmmQuoteResponse | JamQuoteResponse
) -> tuple[HexStr, bool]:
    raw_tx: HexBytes = await quote.sign_transaction(web3=web3, account=account)
    tx_hash = AsyncWeb3.to_hex(await web3.eth.send_raw_transaction(raw_tx))
    LOGGER.info(tx_hash)

    retries: int = 1
    success: bool = False
    while True:
        try:
            receipt = await web3.eth.get_transaction_receipt(tx_hash)
        except TransactionNotFound:
            status = 0
        else:
            status = receipt["status"]
        retries += 1
        if status == 1:
            success = True
            break
        if retries > 20:
            break
        await asyncio.sleep(0.5)
    if success:
        LOGGER.info(f"Order completed. {chain.tx_link(tx_hash)}")
    else:
        LOGGER.warning("Could not confirm order status")
    return tx_hash, success


async def _post_order(
    env: Env,
    order_url: str,
    chain: Chain,
    order_request: OrderRequest,
    headers: dict[str, Any] | None,
    auth: aiohttp.BasicAuth | None,
) -> OrderResponse:
    result = await send_request(
        env=env,
        method="post",
        url=order_url.format(chain=chain.name),
        json=order_request.model_dump(),
        headers=headers,
        auth=auth,
    )
    return OrderResponse.model_validate(result)


async def _get_order_status(
    env: Env,
    order_status_url: str,
    chain: Chain,
    order_status_request: OrderStatusRequest,
    headers: dict[str, Any] | None,
    auth: aiohttp.BasicAuth | None,
) -> OrderStatusResponse:
    result = await send_request(
        env=env,
        method="get",
        url=order_status_url.format(chain=chain.name),
        params=order_status_request.model_dump(),
        headers=headers,
        auth=auth,
    )
    return OrderStatusResponse.model_validate(result)


async def send_request(
    env: Env,
    url: str,
    method: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    auth: aiohttp.BasicAuth | None = None,
) -> dict[str, Any]:
    if env == Env.TEST and not auth:
        raise ValueError("BasicAuth is required for test environment")
    url = url if env == Env.PROD else url.replace("api", "api-test")
    session = aiohttp.ClientSession(headers=headers, auth=auth)
    async with session:
        if method.lower() == "get":
            async with session.get(url, params=params) as response:
                if not response.ok:
                    raise Exception(f"Failed to send GET request: {response.status} - {response.reason}")
                result: dict[str, Any] = await response.json()
                if ERROR_KEY in result:
                    raise Exception(f"Failed to get valid response: {result[ERROR_KEY]}")
                return result
        elif method.lower() == "post":
            async with session.post(url, json=json) as response:
                if not response.ok:
                    raise Exception(f"Failed to send POST request: {response.status} - {response.reason}")
                result = await response.json()
                if ERROR_KEY in result:
                    raise Exception(f"Failed to get valid response: {result[ERROR_KEY]}")
                return result
        else:
            raise ValueError("Unsupported HTTP method. Use 'get' or 'post'.")
