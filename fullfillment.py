from telethon import TelegramClient, events
import random
import asyncio

api_id = 25351228  # Ваш API ID
api_hash = '0119847ee0bf52185c7ae937dd36346f'  # Ваш API Hash

client = TelegramClient('anon', api_id, api_hash)

keywords = ['хай', 'как', 'привет', "так", "я", "мы", "вакансия"]

user_to_notify = 700326689  # Ваш User ID

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if any(keyword.lower() in event.raw_text.lower() for keyword in keywords):
        sender = await event.get_sender()
        sender_name = getattr(sender, 'first_name', 'Нет имени')
        if hasattr(sender, 'last_name') and sender.last_name:
            sender_name += f" {sender.last_name}"
            
        sender_username = f"@{sender.username}" if sender.username else f"tg://openmessage?user_id={sender.id}"

        message_to_send = f"Сообщение от: {sender_name}\nСсылка на профиль: {sender_username}\n\nТекст сообщения:\n{event.raw_text}"
        
        try:
            # Добавляем рандомную задержку перед отправкой сообщения
            delay = random.uniform(5, 30)  # Задержка от 1 до 5 секунд
            await asyncio.sleep(delay)
            await client.send_message(user_to_notify, message_to_send)
        except Exception as e:
            print(f"Произошла ошибка при отправке сообщения: {e}")

client.start()
client.run_until_disconnected()