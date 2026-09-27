import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в Environment Variables")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ---------- HTTP-сервер для Render ----------

async def health_check(request):
    return web.Response(text="TurboVPN Bot is running!")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()

    print(f"HTTP server started on port {port}")


# ---------- Клавиатуры ----------

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔑 Купить ключ")],
        [KeyboardButton(text="📂 Мои ключи")]
    ],
    resize_keyboard=True
)

tariff_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="30 дней — 100 ₽")],
        [KeyboardButton(text="90 дней — 300 ₽")],
        [KeyboardButton(text="180 дней — 500 ₽")],
        [KeyboardButton(text="365 дней — 1000 ₽")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)


# ---------- Команды ----------

@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "🚀 TurboVPN\n\n"
        "Быстрый и стабильный VPN для комфортного доступа к интернету.\n\n"
        "📊 Сейчас с нами:\n"
        "👥 500+ пользователей\n"
        "🔑 123 активные подписки\n"
        "🟢 Все серверы работают\n\n"
        "✨ Возможности:\n"
        "• Умная маршрутизация для российских банков и Госуслуг\n"
        "• Безлимитный трафик\n"
        "• Сервер в Германии\n"
        "• Можно использовать на нескольких устройствах\n\n"
        "Нажмите кнопку ниже, чтобы продолжить."
    )

    await message.answer(text, reply_markup=main_keyboard)


@dp.message(F.text == "🔑 Купить ключ")
async def buy_key(message: Message):
    text = (
        "🔑 Выберите тариф:\n\n"
        "30 дней — 100 ₽\n"
        "90 дней — 300 ₽\n"
        "180 дней — 500 ₽\n"
        "365 дней — 1000 ₽"
    )

    await message.answer(text, reply_markup=tariff_keyboard)


@dp.message(F.text.in_({
    "30 дней — 100 ₽",
    "90 дней — 300 ₽",
    "180 дней — 500 ₽",
    "365 дней — 1000 ₽"
}))
async def payment(message: Message):
    await message.answer(
        "💳 Оплата\n\n"
        "Система оплаты пока находится в разработке.\n"
        "После подключения оплаты здесь появится кнопка для покупки VPN."
    )


@dp.message(F.text == "📂 Мои ключи")
async def my_keys(message: Message):
    await message.answer(
        "📂 Мои ключи\n\n"
        "У вас пока нет активных VPN-ключей."
    )


@dp.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=main_keyboard
    )


# ---------- Запуск ----------

async def main():
    await start_web_server()

    print("Telegram bot started!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
