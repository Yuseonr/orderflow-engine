import aiohttp
import asyncio
from utils.logger import ENGINE_LOGGER

ASUKA_WEBHOOK_URL = "http://127.0.0.1:8080/signal"

async def send_to_asuka(payload: dict):
    try:

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2.0)) as session:
            async with session.post(ASUKA_WEBHOOK_URL, json=payload) as response:

                if response.status == 200:
                    ENGINE_LOGGER.info(f"Successfully pushed {payload['signal']['name']} payload to Asuka.")
                else:
                    ENGINE_LOGGER.warning(f"Asuka server returned status {response.status}")
                    
    except Exception as e:
        ENGINE_LOGGER.error(f"Error sending payload: {e}")

async def webhook_worker(webhook_queue: asyncio.Queue):
    ENGINE_LOGGER.info("Asuka Webhook Started")
    while True:
        try:
    
            payload = await webhook_queue.get()
            await send_to_asuka(payload)
            webhook_queue.task_done()
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            ENGINE_LOGGER.error(f"Webhook worker failed to send: {e}")