from __future__ import annotations

import typing
import time

from ctc import binary
from ctc import spec

from . import block_crud


async def async_print_block_summary(
    block: spec.Block | spec.BlockNumberReference,
    provider: spec.ProviderReference = None,
) -> None:

    import toolstr
    import tooltime

    from ctc import cli

    if not isinstance(block, dict):
        block = await block_crud.async_get_block(block=block, provider=provider)

    full_transactions = len(block['transactions']) > 0 and isinstance(
        block['transactions'][0], dict
    )
    percentiles = [
        0,
        5,
        50,
        95,
        100,
    ]

    if full_transactions:
        gas_prices = [
            typing.cast(spec.Transaction, transaction)['gas_price'] / 1e9
            for transaction in block['transactions']
        ]
        import numpy as np

        gas_percentiles = np.percentile(
            gas_prices,
            percentiles,
        )

    title = 'Block ' + str(block['number'])
    styles = cli.get_cli_styles()
    toolstr.print_text_box(title, style=styles['title'])
    cli.print_bullet(key='timestamp', value=block['timestamp'])
    cli.print_bullet(key='time', value=tooltime.timestamp_to_iso(block['timestamp']))
    cli.print_bullet(
        key='age',
        value=tooltime.timelength_to_phrase(
            round(time.time()) - block['timestamp']
        ),
    )
    cli.print_bullet(key='block_hash', value=block['hash'])
    cli.print_bullet(key='n_transactions:', value=len(block['transactions']))
    cli.print_bullet(
        key='gas used',
        value=(
            toolstr.format(block['gas_used'])
            + '/'
            + toolstr.format(block['gas_limit'])
        ),
    )
    if full_transactions:
        percentile_label = (
            '('
            + ', '.join([str(percentile) + '%' for percentile in percentiles])
            + ')'
        )
        gas_percentiles_str = (
            '('
            + ', '.join(
                [toolstr.format(percentile) for percentile in gas_percentiles]
            )
            + ')'
        )
        print('- gas prices:', percentile_label, '=', gas_percentiles_str)

    message = block['extra_data']
    try:
        message = binary.convert(message, 'binary').decode()
    except Exception as e:
        if len(message) > 80:
            message = message[:77] + '...'
        else:
            message = message
    cli.print_bullet(key='message', value=message)
