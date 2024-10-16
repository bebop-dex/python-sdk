from __future__ import annotations

import os
from typing import TYPE_CHECKING

import aiohttp
import pytest
from dotenv import load_dotenv
from eth_account import Account
from eth_account.account import LocalAccount

from python_sdk.common.types.types import Chain, Env
from python_sdk.jam.client import JamClient
from python_sdk.pmm.client import PMMClient

if TYPE_CHECKING:
    from _pytest.config.argparsing import Parser

load_dotenv()

LOGIN: str | None = os.getenv("LOGIN")
PASSWORD: str | None = os.getenv("PASSWORD")
PRIVATE_KEY: str | None = os.getenv("PRIVATE_KEY")
AUTH: aiohttp.BasicAuth | None = aiohttp.BasicAuth(login=LOGIN, password=PASSWORD) if LOGIN and PASSWORD else None


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--chain-id",
        action="store",
        type=int,
        help="Chain ID",
        dest="CHAINID",
        choices=[chain.id for chain in Chain],
    )
    parser.addoption(
        "--solver",
        action="store",
        type=str,
        dest="SOLVER",
        help="Your solver emoji",
    )
    parser.addoption(
        "--maker",
        action="store",
        type=str,
        dest="MAKER",
        help="Your maker emoji, suffix with 'T' for self-execution, or 'F' for fast mode",
    )
    parser.addoption(
        "--gasless",
        action="store",
        type=str,
        dest="GASLESS",
        help="Whether the order is sent in gasless or self-execution mode",
    )
    parser.addoption(
        "--rpc",
        action="store",
        type=str,
        dest="RPC",
        help="The RPC URL if you want to override the default public RPC for the chain",
    )
    parser.addoption(
        "--env",
        action="store",
        type=str,
        dest="ENV",
        help="Environment (PROD / TEST)",
        choices=[env.value for env in Env],
    )


@pytest.fixture(scope="session", autouse=True)
def chain(request: pytest.FixtureRequest) -> Chain:
    chain_value = request.config.option.CHAINID
    return Chain(chain_value)


@pytest.fixture(scope="session", autouse=True)
def solver(request: pytest.FixtureRequest) -> str:
    solver: str = request.config.option.SOLVER
    return solver


@pytest.fixture(scope="session", autouse=True)
def maker(request: pytest.FixtureRequest) -> str:
    maker: str = request.config.option.MAKER
    return maker


@pytest.fixture(scope="session", autouse=True)
def gasless(request: pytest.FixtureRequest) -> bool:
    gasless: str = request.config.option.GASLESS
    return gasless.lower() == "true"


@pytest.fixture(scope="session", autouse=True)
def rpc(request: pytest.FixtureRequest) -> str:
    rpc_url: str = request.config.option.RPC
    return rpc_url


@pytest.fixture(scope="session", autouse=True)
def env(request: pytest.FixtureRequest) -> Env:
    env: str = request.config.option.ENV
    return Env(env.upper())


@pytest.fixture(scope="session", autouse=True)
def jam(chain: Chain, rpc: str, env: Env) -> JamClient:
    return JamClient(chain=chain, private_key=PRIVATE_KEY, rpc_url=rpc if rpc else chain.public_rpc, env=env, auth=AUTH)


@pytest.fixture(scope="session", autouse=True)
def pmm(chain: Chain, rpc: str, env: Env) -> PMMClient:
    return PMMClient(chain=chain, private_key=PRIVATE_KEY, rpc_url=rpc if rpc else chain.public_rpc, env=env, auth=AUTH)


@pytest.fixture(scope="session", autouse=True)
def account() -> LocalAccount:
    account: LocalAccount = Account.from_key(PRIVATE_KEY)
    return account
