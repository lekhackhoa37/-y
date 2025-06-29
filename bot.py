import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message

# === Cấu hình bot ===
api_id = 28566251
api_hash = "232a0b761e7b322de8a30727f3563cfc"
session_name = "user_forwarder_session"

SOURCE_CHAT_ID = -1002487333004
TARGET_CHAT_ID = -1001234567890

# === Kiểm tra file session có tồn tại không (debug trên Render) ===
if not os.path.exists(f"{session_name}.session"):
    print(f"❌ Không tìm thấy file session: {session_name}.session")
    print("➡️ Bạn cần tạo file session trên máy cá nhân, rồi push lên Git bằng lệnh:")
    print(f"   git add {session_name}.session --force && git commit -m 'add session' && git push")
else:
    print(f"✅ Đã tìm thấy file session: {session_name}.session")

# === Khởi tạo Pyrogram Client ===
app = Client(
    session_name,
    api_id=api_id,
    api_hash=api_hash
)

# === Hàm xử lý tin nhắn chứa video hoặc ảnh ===
@app.on_message(filters.chat(SOURCE_CHAT_ID) & (filters.video | filters.photo))
async def forward_media(client: Client, message: Message):
    try:
        print(f"[{message.date}] Nhận media từ {message.chat.title or message.chat.first_name} (ID: {message.chat.id})")
        await message.copy(TARGET_CHAT_ID, caption="cập nhật mới nhất")
        print(f"[{message.date}] ✅ Đã chuyển tiếp media (ID: {message.id})")
    except Exception as e:
        print(f"❌ Lỗi khi chuyển tiếp media (ID: {message.id}): {e}")

# === Hàm chạy chính của bot ===
async def main():
    print("🚀 Khởi động bot user...")
    await app.start()

    user_info = await app.get_me()
    print(f"🟢 Bot User: {user_info.first_name} (@{user_info.username or 'Không có username'})")
    print(f"🆔 ID tài khoản: {user_info.id}")
    print("📡 Bot đang lắng nghe tin nhắn...")

    await idle()
    await app.stop()
    print("⛔ Bot đã dừng.")

# === Điểm khởi chạy ===
if __name__ == "__main__":
    asyncio.run(main())
