import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiohttp import web

TOKEN = "8386838255:AAGURM4ADU3VAjPm4n8t6_DhROSwGYaq-yA"

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

WEBHOOK_PATH = "/webhook"

# ❗❗ آدرس وبهوک باید آدرس رسمی Render باشد:
# https://YOUR-SERVICE.onrender.com/webhook
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_URL = RENDER_URL + WEBHOOK_PATH


@router.message()
async def echo(message):
    await message.reply("سلام ابوذر! ربات webhook فعاله.")


app = web.Application()


async def handle(request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response()


app.router.add_post(WEBHOOK_PATH, handle)


async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(app):
    await bot.delete_webhook()


app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)
