import json
import logging
from typing import Any, Dict

from aiohttp import ClientSession

from brief.utils.decorators import ATimedMemo

logger = logging.getLogger(__name__)
name = "bitcoin_coindesk"


@ATimedMemo(minutes=1)
async def get_btc(session: ClientSession) -> Dict[str, Any]:
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    async with session.get(url) as resp:
        if resp.status == 200:
            # coindesk api returns the application/javascript content type
            # this breaks aiohttp's json method
            return json.loads(await resp.text())


async def run_brief(session: ClientSession):
    return await get_btc(session)
