import json
import ngrok
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from pymongo import MongoClient

from config import TELEGRAM_TOKEN
from models import MessageData
from utils import aggregate

WEBHOOK_PATH = f"/bot/{TELEGRAM_TOKEN}"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

client = MongoClient("mongodb://mongo_service:27017")
db = client["sample_db"]
collection = db['sample_collection']
print(client.list_database_names())
print(db.list_collection_names())

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
        message_data = MessageData(
            dt_from=json_object["dt_from"],
            dt_upto=json_object["dt_upto"],
            group_type=json_object["group_type"]
        )
        out_msg = aggregate(message_data, collection)
        await bot.send_message(chat_id, json.dumps(out_msg))
    except Exception:
        await bot.send_message(chat_id, "something wrong")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
