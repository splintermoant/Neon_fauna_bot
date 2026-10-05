import logging
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Загружаем токен из файла .env для безопасности
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN", "8672778966:AAFBmFpHLtWVudBKoNSg6u8t6fNlbyT15-g") 
BOT_USERNAME = "GenMint_bot"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Временная база данных в оперативной памяти
users_db = {}

NFT_MARKETPLACE = [
    {
        "id": 1,
        "name": "NextGen Cyber Bear #1",
        "price": "5 TON",
        # Прямая ссылка на тестовое изображение aiogram (замените на свою картинку .jpg/.png)
        "image": "https://githubusercontent.com", 
        "buy_url": "https://getgems.io"
    }
]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    command_args = message.text.split()
    
    if user_id not in users_db:
        referred_by = None
        # Проверяем, передал ли пользователь реферальный ID (например, /start 123456)
        if len(command_args) > 1:
            try:
                referrer_id = int(command_args[1])
                if referrer_id != user_id:
                    referred_by = referrer_id
            except ValueError:
                pass
        
        users_db[user_id] = {"referred_by": referred_by, "points": 0}
        
        # Начисляем бонусы пригласителю
        if referred_by and referred_by in users_db:
            users_db[referred_by]["points"] += 10
            try:
                await bot.send_message(
                    chat_id=referred_by,
                    text="🎉 По вашей ссылке зарегистрировался новый участник! Вам начислено **10 NG-бонусов**.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                logging.error(f"Не удалось отправить уведомление рефереру: {e}")

    await message.answer(
        f"⚡️ **Приветствуем в NextGen_NFT!** ⚡️\n\n"
        f"Вы попали на маркетплейс цифрового искусства нового поколения.\n\n"
        f"🤖 **Используйте меню или команды:**\n"
        f"• /catalog — Показать NFT коллекции\n"
        f"• /invite — Пригласить друзей и заработать бонусы\n"
        f"• /earn — Способы заработка на наших токенах",
        parse_mode="Markdown"
    )

@dp.message(Command("catalog"))
async def cmd_catalog(message: types.Message):
    for nft in NFT_MARKETPLACE:
        builder = InlineKeyboardBuilder()
        builder.button(text=f"Купить за {nft['price']}", url=nft['buy_url'])
        caption = f"🎨 **{nft['name']}**\n💰 Цена: {nft['price']}\n\n🤖 *Эксклюзивно в NextGen NFT*"
        try:
            # Отправляем фото с кнопкой
            await message.answer_photo(
                photo=nft['image'], 
                caption=caption, 
                reply_markup=builder.as_markup(), 
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Ошибка отправки фото: {e}. Отправляем текст.")
            # Если ссылка на фото сломалась, отправляем текстовую заглушку с кнопкой
            await message.answer(
                f"{caption}\n🔗 Ссылка: {nft['buy_url']}", 
                reply_markup=builder.as_markup(),
                parse_mode="Markdown"
            )

@dp.message(Command("invite"))
async def cmd_invite(message: types.Message):
    user_id = message.from_user.id
    
    # Если старый пользователь введет команду после перезапуска бота
    if user_id not in users_db:
        users_db[user_id] = {"referred_by": None, "points": 0}
        
    user_data = users_db[user_id]
    # Исправлена ссылка: добавлен слэш после t.me/
    ref_link = f"https://t.me{BOT_USERNAME}?start={user_id}"
    
    await message.answer(
        "👥 **Реферальная программа NextGen NFT**\n\n"
        f"🔗 **Ваша ссылка для приглашения:**\n`{ref_link}`\n\n"
        f"💰 Ваш баланс: **{user_data['points']} NG-бонусов**\n\n"
        "🎁 **На что можно обменять бонусы:**\n"
        "• 50 бонусов = Скидка 50% на любой NFT\n"
        "• 100 бонусов = 1 Бесплатный секретный NFT-бокс!",
        parse_mode="Markdown"
    )

@dp.message(Command("earn"))
async def cmd_earn(message: types.Message):
    await message.answer(
        "📈 **Как зарабатывать с NextGen NFT?**\n\n"
        "1. **Флиппинг (Перепродажа):** Покупайте редкие экземпляры на старте продаж и продавайте дороже на маркетплейсах.\n"
        "2. **Роялти холдеров:** Купите премиум-NFT из нашего каталога и получайте пассивный доход в криптовалюте от общего оборота проекта.\n"
        "3. **Реферальный заработок:** Копите бонусы через команду /invite и обменивайте их на реальные цифровые активы бесплатно!",
        parse_mode="Markdown"
    )

async def main():
    # Запуск бота в режиме постоянного опроса (polling)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
