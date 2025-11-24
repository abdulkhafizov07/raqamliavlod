from aiogram import Dispatcher, F
from aiogram.types import Message
from asgiref.sync import sync_to_async
from news.models import News
from bot.config import bot,dp

from django.conf import settings


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    from aiogram.types import WebAppInfo
    web_app_info = WebAppInfo(url="https://telegrambot.ithubacademy.uz")
    await message.answer(
        "👋 Hello! I'm your Django + Aiogram bot.",
        reply_markup={
            "keyboard": [
                [{"text": "Open Web App", "web_app": web_app_info}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
    )
@dp.channel_post(F.chat.id == settings.TG_CHANNEL_ID)
async def channel_post_handler(message: Message):
    # get image from message
    # download the image into MEDIA_ROOT/news/
    from django.conf import settings
    import os
    print(message.caption)
    if not message.photo or not message.caption:
        return
    if message.photo:   
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, destination=os.path.join(settings.MEDIA_ROOT, 'news', f'{message.message_id}.jpg'))
        file_path = os.path.join('news', f'{message.message_id}.jpg')
        # Save the news item to the database
        title = [line for line in message.caption.split('\n') if not line.strip().startswith('#') and line][0] if message.caption else " "
        # if the message is forwarded, use original message posted time
        if message.forward_origin:
            print("Forwarded message")
            time = message.forward_origin.date
        else:
            time = message.date
        await sync_to_async(News.objects.create)(
                title=title,
                image=file_path,
                time=time,
                tg_url=f'https://t.me/c/{str(channel_id)[4:]}/{message.message_id}'
            )