import toolstr

from ctc import evm
from ctc import rpc


def get_command_spec():
    return {
        'f': async_balance_command,
        'help': 'output ETH balance of address',
        'args': [
            {'name': 'address', 'help': 'address of wallet'},
            {'name': '--block', 'help': 'block number'},
            {
                'name': '--raw',
                'action': 'store_true',
                'help': 'skip normalizing balance by 1e18 decimals',
            },
        ],
    }


async def async_balance_command(address, block, raw):

    if block is not None:
        block = await evm.async_block_number_to_int(block)

    balance = await evm.async_get_eth_balance(
        address=address,
        block=block,
        normalize=(not raw),
    )
    if raw:
        print(balance)
    else:
        print(toolstr.format(balance))
    await rpc.async_close_http_session()

