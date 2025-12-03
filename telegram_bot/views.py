import json
import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from aiogram.types import Update
from bot.config import bot
from bot.handlers import dp

@csrf_exempt
async def telegram_webhook(request):
    if request.method == "POST":
        data = request.body
        update = Update.model_validate(json.loads(data))
        await dp.feed_update(bot, update, skip_updates=True)
        return JsonResponse({"ok": True})
    return JsonResponse({"error": "Only POST method allowed"}, status=405)
