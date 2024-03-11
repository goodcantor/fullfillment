from telethon import TelegramClient, events
import random
import asyncio

api_id = 25351228
api_hash = '0119847ee0bf52185c7ae937dd36346f'

client = TelegramClient('anon', api_id, api_hash)

keywords = [
    'фуллфилмент', 'фулфилмент', 'фуллфилимент', 'фулфилимент', 'ффилмент', 'фулфилметн', "фф",
    'фулфелмент', 'фулфиллмент', 'фулфилмен', 'фулфилмет', 'фуллфилмет', 'фулфилимнет',
]

# Массив ID пользователей, которым будут отправлены уведомления
users_to_notify = [700326689, 1020324564]  

banned_usernames = ['grouphelpbot']  

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        # Если сообщение пришло в личные сообщения, то пропускаем его
        return

    sender = await event.get_sender()
    sender_username = sender.username.lower() if sender.username else ''
    message_id = event.id
    chat = await event.get_chat()
    chat_id = chat.id
    
    if sender.username.lower()[-3:] == 'bot':
      return

    # Преобразование отрицательного ID чата в формат ссылки
    if chat_id < 0:
        chat_id = str(chat_id)[4:]

    # Создание URL для сообщения
    message_link = f"https://t.me/c/{chat_id}/{message_id}"

    if sender_username not in banned_usernames and any(keyword.lower() in event.raw_text.lower() for keyword in keywords):
        sender_name = getattr(sender, 'first_name', 'Нет имени')
        if hasattr(sender, 'last_name') and sender.last_name:
            sender_name += f" {sender.last_name}"

        profile_link = f"@{sender_username}" if sender.username else f"tg://openmessage?user_id={sender.id}"

        message_to_send = (
            f"Сообщение от: {sender_name}\n"
            f"Ссылка на профиль: {profile_link}\n"
            f"Ссылка на сообщение: {message_link}\n\n"
            f"Текст сообщения:\n{event.raw_text}"
        )

        for user_id in users_to_notify:
            try:
                # Добавляем рандомную задержку перед отправкой сообщения
                delay = random.uniform(5, 15)
                await asyncio.sleep(delay)
                await client.send_message(user_id, message_to_send)
            except Exception as e:
                print(f"Произошла ошибка при отправке сообщения пользователю {user_id}: {e}")

client.start()
client.run_until_disconnected()