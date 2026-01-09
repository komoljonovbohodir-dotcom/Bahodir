import asyncio
import logging
import sys,os bahodir20

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from  dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()
API=os.getenv("API")
Chat=os.getenv("Chat")

dp = Dispatcher()
os.makedirs("id/step", exist_ok=True)

ortga = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Orqaga")]],
    resize_keyboard=True
)

def get_step(user_id):
    path = f"id/step/{user_id}.txt"
    if os.path.exists(path):
        return open(path).read().strip()
    return None


def set_step(user_id, step):
    open(f"id/step/{user_id}.txt", "w").write(step)

def del_step(user_id):
    path = f"id/step/{user_id}.txt"
    if os.path.exists(path):
        os.remove(path)

async def CHAT(s:str):
    with Mistral(
            api_key=Chat,
    ) as mistral:
        res = mistral.chat.complete(model="mistral-small-latest", messages=[
            {
                "content": s+"uz language",
                "role": "user",
            },
        ], stream=False)

        return res.choices[0].message.content


@dp.message(Command('start'))
async def command_start_handler(msg: Message) -> None:
    await msg.answer(f"Salom, {html.bold(msg.from_user.full_name)}!")
    await msg.answer(
        "*Rasm mavzusini yuboring, yani nima haqida rasm kerak.*",
        reply_markup=ortga,
        parse_mode="Markdown"
    )



@dp.message()
async def echo_handler(msg: Message,bot:Bot) -> None:
    set_step(msg.from_user.id, "photo")
    user_id = msg.from_user.id
    step = get_step(user_id)

    if step == "photo":
        query = msg.text
        photo_url = f"https://yandex.uz/images/touch/search/?text={query}"

        await bot.send_photo(
            chat_id=user_id,
            photo=photo_url,
            caption=f"📸<b> Rasm topildi!\n\n🖼 Rasm mavzusi: {query}</b>",
            reply_markup=ortga,
            parse_mode="HTML"
        )
        await msg.answer(await CHAT(query))

        del_step(user_id)



async def main() -> None:
    bot = Bot(token=API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())


