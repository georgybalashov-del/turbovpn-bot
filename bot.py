import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ---------- Клавиатуры ----------

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Далее", callback_data="next")]
        ]
    )


def main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔑 Купить ключ", callback_data="buy")],
            [InlineKeyboardButton(text="📂 Мои ключи", callback_data="keys")],
        ]
    )


def tariffs_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="30 дней — 100 ₽", callback_data="tariff_30")],
            [InlineKeyboardButton(text="90 дней — 300 ₽", callback_data="tariff_90")],
            [InlineKeyboardButton(text="180 дней — 500 ₽", callback_data="tariff_180")],
            [InlineKeyboardButton(text="365 дней — 1000 ₽", callback_data="tariff_365")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="home")],
        ]
    )


def payment_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", callback_data="payment")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="buy")],
        ]
    )


# ---------- /start ----------

@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "🚀 <b>Turbo VPN</b>\n\n"
        "Премиальный VPN для быстрого и приватного интернета.\n"
        "Безлимитный трафик и никаких ограничений.\n\n"
        "👥 Пользователей: <b>500+</b>\n"
        "🔑 Активных подписок: <b>123</b>\n"
        "🟢 Статус серверов: <b>всё работает</b>\n\n"
        "🔥 <b>Почему Turbo VPN?</b>\n\n"
        "• 🧠 Умная маршрутизация — не нужно отключать VPN "
        "для Госуслуг, банков и других российских сервисов.\n"
        "• ♾️ Безлимитный трафик — игры, видео и большие файлы.\n"
        "• 🇩🇪 Сервер в Германии.\n"
        "• 📱 Безлимитное количество устройств.\n\n"
        "Нажмите «Далее», чтобы открыть главное меню."
    )

    await message.answer(
        text,
        reply_markup=start_keyboard(),
        parse_mode="HTML"
    )


# ---------- Главное меню ----------

@dp.callback_query(F.data == "next")
async def next_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите нужный раздел:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "home")
async def home(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите нужный раздел:",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# ---------- Покупка ----------

@dp.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔑 <b>Выберите тариф</b>\n\n"
        "Доступ к Turbo VPN:",
        reply_markup=tariffs_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


tariffs = {
    "tariff_30": ("30 дней", "100 ₽"),
    "tariff_90": ("90 дней", "300 ₽"),
    "tariff_180": ("180 дней", "500 ₽"),
    "tariff_365": ("365 дней", "1000 ₽"),
}


@dp.callback_query(F.data.in_(tariffs.keys()))
async def choose_tariff(callback: CallbackQuery):
    name, price = tariffs[callback.data]

    await callback.message.edit_text(
        f"🔑 <b>Тариф: {name}</b>\n\n"
        f"💰 Стоимость: <b>{price}</b>\n\n"
        "После оплаты вы получите VPN-ключ.\n\n"
        "💳 Оплата пока находится в режиме тестирования.",
        reply_markup=payment_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# ---------- Тестовая оплата ----------

@dp.callback_query(F.data == "payment")
async def payment(callback: CallbackQuery):
    await callback.message.edit_text(
        "💳 <b>Оплата</b>\n\n"
        "Это тестовая версия бота.\n"
        "Настоящая банковская оплата будет подключена позже.\n\n"
        "🔧 Сейчас можно проверить только работу меню и тарифов.",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# ---------- Мои ключи ----------

@dp.callback_query(F.data == "keys")
async def my_keys(callback: CallbackQuery):
    await callback.message.edit_text(
        "📂 <b>Мои ключи</b>\n\n"
        "У вас пока нет активных VPN-ключей.",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


# ---------- Запуск ----------

async def main():
    print("Turbo VPN bot запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
