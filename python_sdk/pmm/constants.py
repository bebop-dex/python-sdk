from eth_utils.address import to_checksum_address

from python_sdk.common.constants import BASE_URL
from python_sdk.common.types.types import Chain

PMM_SETTLEMENT_ADDRESS = to_checksum_address("0xbbbbbBB520d69a9775E85b458C58c648259FAD5F")

SUPPORTED_CHAINS = {Chain.ethereum, Chain.polygon, Chain.arbitrum, Chain.blast, Chain.optimism, Chain.blast}

API_VERSION = 3
QUOTE_URL = BASE_URL + "/pmm/{chain}/" + f"v{API_VERSION}/quote"
ORDER_URL = BASE_URL + "/pmm/{chain}/" + f"v{API_VERSION}/order"
ORDER_STATUS_URL = BASE_URL + "/pmm/{chain}/" + f"v{API_VERSION}/order-status"
