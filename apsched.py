from aiogram import Bot


async def send_message_cron(bot: Bot):
    await bot.send_message(882786125, f'fgdfgdfgd')


async def send_message_time(bot: Bot):
    await bot.send_message(882786125, f'Через 3 секунды')
