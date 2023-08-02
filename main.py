import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bs4 import BeautifulSoup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import apsched
from datetime import datetime, timedelta
import asyncio

URL = 'https://coinranking.com/ru'


def priceB(url):
    r = requests.get(url)
    rows = BeautifulSoup(r.text, "html.parser")
    price = rows.find("td", class_="table__cell--responsive")
    if price:
        price = str(price.find("div", class_="valuta--light").text \
                    .replace("$", "").replace(",", ".").replace(" ", "") \
                    .replace("\n", "").replace("\xa0", ""))
    return price


list_of_prices = priceB(URL)

token = '5845830403:AAE1vfWj0djacPcRD3Ysepv7CTuk9WA6j9U'


async def start_bot(bot: Bot):
    await bot.send_message(882786125, text="Бот запущен!")


async def stop_bot(bot: Bot):
    await bot.send_message(882786125, text="Бот остановлен!")


async def get_start(message: Message, bot: Bot):
    await bot.send_message(882786125, priceB(URL))


async def start():
    bot = Bot(token=token, parse_mode='HTML')

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=3),
                      kwargs={'bot': bot})
    scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour,
                      minute=datetime.now().minute + 1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()


if __name__ == "__main__":
    asyncio.run(start())
