import asyncio
from collections.abc import Coroutine
from typing import Any

from eth_account.account import LocalAccount
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.types import TxParams, Wei

from python_sdk.common.constants import ERC20_ABI
from python_sdk.common.utils.logger import Logger

LOGGER = Logger(__name__)


async def gather_with_concurrency(n: int, *tasks: Coroutine) -> list[Any]:
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task: Coroutine) -> Any:
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def approve_token(
    web3: AsyncWeb3, account: LocalAccount, token_address: str, amount: int, spender: str
) -> HexBytes:
    token_contract = web3.eth.contract(AsyncWeb3.to_checksum_address(token_address), abi=ERC20_ABI)
    input_data = token_contract.encodeABI(fn_name="approve", args=[spender, amount])
    nonce = await web3.eth.get_transaction_count(account.address)
    data = TxParams(
        **{
            "from": account.address,
            "chainId": await web3.eth.chain_id,
            "nonce": nonce,
            "gasPrice": Wei(int(await web3.eth.gas_price * 1.5)),
            "data": input_data,
            "value": Wei(0),
            "to": token_address,
        }
    )
    gas_estimate = await web3.eth.estimate_gas(data)
    data["gas"] = gas_estimate
    signed_tx: SignedTransaction = web3.eth.account.sign_transaction(transaction_dict=data, private_key=account.key)
    result = await web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    await web3.eth.wait_for_transaction_receipt(result)
    LOGGER.info(f"Approved {amount=} for {token_address=} on {spender=}")
    return result


async def revoke_token(web3: AsyncWeb3, account: LocalAccount, token_address: str, spender: str) -> HexBytes:
    return await approve_token(web3, account, token_address, 0, spender)
