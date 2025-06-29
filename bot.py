from pyrogram import Client, filters
from pyrogram.types import Message

# Thông tin session từ tài khoản Telegram cá nhân
api_id = 28566251
api_hash = "232a0b761e7b322de8a30727f3563cfc"
session_name = "+13192846724"  # KHÔNG cần .session, chỉ tên thôi (file .session bạn đã có)

# ID nhóm nguồn và nhóm đích
SOURCE_CHAT_ID = -1002487333004  # Nhóm nguồn (bạn đã tham gia bằng acc người thật)
TARGET_CHAT_ID = -1001234567890  # Nhóm đích (bạn làm admin)

# Tạo app Pyrogram
app = Client(session_name, api_id=api_id, api_hash=api_hash)

# Hàm xử lý forward video hoặc ảnh
@app.on_message(filters.chat(SOURCE_CHAT_ID) & (filters.video | filters.photo))
async def forward_media(client: Client, message: Message):
    await message.copy(chat_id=TARGET_CHAT_ID, caption="Cập nhật mới nhất")

# Chạy app
app.run()
