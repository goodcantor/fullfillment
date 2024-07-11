from telethon import TelegramClient, events
import random
import asyncio

api_id = 27306467
api_hash = '5eab758cd12ae881e7f12e19259d5ba9'

client = TelegramClient('anon', api_id, api_hash)

keywords = [
    'фуллфилмент', 'фулфилмент', 'фуллфилимент', 'фулфилимент', 'ффилмент', 'фулфилметн', "фф",
    'фулфелмент', 'фулфиллмент', 'фулфилмен', 'фулфилмет', 'фуллфилмет', 'фулфилимнет', 'филмент', 'филлмент'
]

banned_words = [
    'графического',
    'графический',
    'графика',
    'предлагаю',
    'предлагает',
    'предлагаем',
    'предлагаете',
    'предлагают',
    'предложил',
    'предложила',
    'предложило',
    'предложили',
    'предложить',
    'предложу',
    'предложим',
    'предложишь',
    'предложите',
]
channel_id = -1002070130553  # ID Telegram канала, куда будут отправляться уведомления

banned_usernames = ['grouphelpbot', 'bgdnbgdn', 'birinim', 'zamerova21', 'Jose8Per', 'Tagranovich', 'bgdnbgdn']

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
    
    if sender_username.endswith('bot') or (len(event.raw_text) > 200):
        return
      
    if any(banned_word.lower() in event.raw_text.lower() for banned_word in banned_words):
        return

    # Преобразование отрицательного ID чата в формат ссылки
    if chat_id < 0:
        chat_id = f"-100{str(chat_id)[4:]}"
        
    chat_link = f"https://t.me/{chat.username}" if chat.username else f"tg://openmessage?chat_id={chat_id}"

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
            f"Ссылка на сообщение: {message_link}\n"
            f"Ссылка на чат: {chat_link}\n\n"
            f"Текст сообщения:\n{event.raw_text}"
        )

        try:
            # Добавляем рандомную задержку перед отправкой сообщения
            delay = random.uniform(10, 35)
            await asyncio.sleep(delay)
            await client.send_message(channel_id, message_to_send)
        except Exception as e:
            print(f"Произошла ошибка при отправке сообщения в канал {channel_id}: {e}")

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())