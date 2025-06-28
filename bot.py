from pyrogram import Client, filters
from pyrogram.types import Message

api_id = 28566251
api_hash = "232a0b761e7b322de8a30727f3563cfc"
session_name = "+13192846724.session"  # file session bạn có

SOURCE_CHAT_ID = -1002487333004  # ID nhóm nguồn
TARGET_CHAT_ID = -1001234567890  # ID nhóm đích bạn muốn gửi

app = Client(session_name, api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(SOURCE_CHAT_ID) & (filters.video | filters.photo))
async def forward_media(client: Client, message: Message):
    if message.video:
        await message.copy(TARGET_CHAT_ID, caption="cập nhật mới nhất")
    elif message.photo:
        await message.copy(TARGET_CHAT_ID, caption="cập nhật mới nhất")

app.run()
