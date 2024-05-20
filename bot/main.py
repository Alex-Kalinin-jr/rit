import asyncio
import json
import ngrok
import datetime
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types

from config import TELEGRAM_TOKEN
from models import MessageData

WEBHOOK_PATH = f"/bot/{TELEGRAM_TOKEN}"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

async def lifespan(app):
    tmp = await ngrok.forward(8000, authtoken_from_env=True)
    forward_url = tmp.url()
    
    WEBHOOK_URL = f"{forward_url}{WEBHOOK_PATH}"

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=WEBHOOK_URL)

    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post(f"{WEBHOOK_PATH}")
async def bot_webhook(update: types.Update):
    chat_id = update.message.chat.id
    try:
        json_object = json.loads(update.message.text)
        message_data = MessageData(text=json_object)

        await bot.send_message(chat_id, "THIS_IS_SPARTA")
    except Exception as e:
        await bot.send_message(chat_id, "something wrong")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
