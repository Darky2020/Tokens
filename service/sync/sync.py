from ..process import process_block, process_reorg
from ..utils import make_request, log_message
from ..process import process_locks
from ..parse import parse_block
from ..chain import get_chain
from tortoise import Tortoise
from ..models import Block
import config

async def sync_chain():
    await Tortoise.init(config=config.tortoise)
    await Tortoise.generate_schemas()

    # Init genesis
    if not (await Block.filter().order_by("-height").limit(1).first()):
        log_message("Adding genesis block to db")

        chain = get_chain(config.chain)

        block_data = await parse_block(chain["genesis"]["height"])

        if block_data["block"]["hash"] != chain["genesis"]["hash"]:
            log_message("Genesis hash missmatch")
            raise

        await process_block(block_data)

    latest = await Block.filter().order_by("-height").limit(1).first()
    chain_data = await make_request("getblockchaininfo")

    # Process chain reorgs
    while latest.hash != await make_request("getblockhash", [latest.height]):
        log_message(f"Found reorg at height #{latest.height}")

        reorg_block = latest
        latest = await Block.filter(
            height=(latest.height - 1)
        ).first()

        await process_reorg(reorg_block)

    display_log = latest.height + 10 > chain_data["blocks"]

    for height in range(latest.height + 1, chain_data["blocks"] + 1):
        try:
            if display_log:
                log_message(f"Processing block #{height}")
            else:
                if height % 100 == 0:
                    log_message(f"Processing block #{height}")

            block_data = await parse_block(height)

            await process_block(block_data)

            await process_locks(height)

        except KeyboardInterrupt:
            log_message(f"Keyboard interrupt")
            break

    await Tortoise.close_connections()
