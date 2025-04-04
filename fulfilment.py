import asyncio
from telethon import TelegramClient, events
import random

# Телеграм API-ключи
api_id = 20290530
api_hash = '605c849a8c71e5952db576c39dd0201a'

# ID канала для уведомлений
channel_id = -1002673291270  

client = TelegramClient('anon', api_id, api_hash)

# Ключевые слова
keywords = [
    'фуллфилмент', 'фулфилмент', 'фуллфилимент', 'фулфилимент', 'ффилмент', 'фулфилметн', "фф",
    'фулфелмент', 'фулфиллмент', 'фулфилмен', 'фулфилмет', 'фуллфилмет', 'фулфилимнет', 'филмент', 'филлмент',
]

# Запрещенные слова
banned_words = [
    'графического', 'графический', 'графика',
    'предлагаю', 'предлагает', 'предлагаем', 'предлагаете', 'предлагают',
    'предложил', 'предложила', 'предложило', 'предложили',
    'предложить', 'предложу', 'предложим', 'предложишь', 'предложите',
]

# Черный список пользователей
banned_usernames = ['grouphelpbot', 'bgdnbgdn', 'birinim', 'zamerova21', 'Jose8Per', 'Tagranovich']

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if event.is_private:
            return

        sender = await event.get_sender()
        chat = await event.get_chat()
        message_id = event.id
        sender_username = getattr(sender, 'username', '').lower() if sender.username else ''
        message_text = getattr(event, 'raw_text', '')

        # Отладочный вывод
        print(f"📩 Новый пост в чате {chat.id}: {message_text[:50]}...")

        # Фильтруем ненужные сообщения
        if sender_username.endswith('bot') or len(message_text) > 200:
            return
        
        if any(word.lower() in message_text.lower() for word in banned_words):
            return

        # Проверка на ключевые слова
        if sender_username not in banned_usernames and any(word.lower() in message_text.lower() for word in keywords):
            sender_name = getattr(sender, 'first_name', 'Нет имени')
            if hasattr(sender, 'last_name') and sender.last_name:
                sender_name += f" {sender.last_name}"

            profile_link = f"@{sender_username}" if sender.username else f"tg://openmessage?user_id={sender.id}"

            # Формируем корректные ссылки
            if chat.username:
                chat_link = f"https://t.me/{chat.username}"
                message_link = f"https://t.me/{chat.username}/{message_id}"
            else:
                chat_id_str = str(chat.id).replace('-100', '')  # Приводим ID к нужному формату
                chat_link = f"tg://resolve?domain={chat.id}"
                message_link = f"https://t.me/c/{chat_id_str}/{message_id}"

            message_to_send = (
                f"🔔 **Новое сообщение!**\n\n"
                f"👤 **От:** {sender_name}\n"
                f"📌 **Профиль:** {profile_link}\n"
                f"📩 **Сообщение:** {message_link}\n"
                f"💬 **Чат:** {chat_link}\n\n"
                f"✉️ **Текст:**\n```{message_text}```"
            )

            # Рандомная задержка перед отправкой сообщения (анти-спам)
            delay = random.uniform(10, 35)
            await asyncio.sleep(delay)

            # Отправляем сообщение
            await client.send_message(channel_id, message_to_send)
            print(f"✅ Сообщение отправлено в {channel_id}")

    except Exception as e:
        print(f"⚠ Ошибка обработки сообщения: {e}")

async def main():
    async with client:
        print("🔵 Бот запущен и слушает события...")
        await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start())
        print("🔵 Бот запущен и слушает события...")
        loop.run_until_complete(client.run_until_disconnected())
    except KeyboardInterrupt:
        print("⛔ Остановка по Ctrl+C")
    finally:
        loop.run_until_complete(client.disconnect())
        loop.close()
