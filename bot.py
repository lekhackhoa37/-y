import os
import asyncio # Thêm thư viện asyncio để chạy bất đồng bộ
from pyrogram import Client, filters, idle # Thêm 'idle' để giữ bot chạy liên tục
from pyrogram.types import Message # Thêm để sử dụng kiểu dữ liệu Message

# === Cấu hình bot ===
# LƯU Ý QUAN TRỌNG:
# 1. api_id và api_hash: Lấy từ my.telegram.org sau khi đăng nhập bằng tài khoản muốn dùng.
# 2. session_name: Đây là tên file sẽ lưu phiên đăng nhập của bạn (ví dụ: my_user_session.session).
#    Bạn PHẢI TỰ TẠO file này MỘT LẦN DUY NHẤT trên máy tính cục bộ của mình,
#    sau đó đẩy lên Git cùng với code. XEM HƯỚNG DẪN BÊN DƯỚI.
#    Không nên đặt tên session là số điện thoại để tránh nhầm lẫn.

api_id = 28566251 # API ID của bạn
api_hash = "232a0b761e7b322de8a30727f3563cfc" # API Hash của bạn
session_name = "user_forwarder_session" # Đặt tên phiên làm việc dễ hiểu.
                                        # File session sẽ có tên: user_forwarder_session.session

# ID nhóm hoặc kênh nguồn mà bot sẽ đọc tin nhắn từ đó
# Đảm bảo bạn đã thêm bot vào nhóm/kênh này và cấp quyền đọc tin nhắn.
SOURCE_CHAT_ID = -1002487333004 

# ID nhóm hoặc kênh đích mà bot sẽ chuyển tiếp tin nhắn đến
# Đảm bảo bạn đã thêm bot vào nhóm/kênh này và cấp quyền gửi tin nhắn.
TARGET_CHAT_ID = -1001234567890 

# Khởi tạo Client của Pyrogram
# Pyrogram sẽ tìm file session_name.session để đăng nhập.
# Nếu không tìm thấy hoặc file bị lỗi, nó sẽ yêu cầu đăng nhập.
app = Client(
    session_name,
    api_id=api_id,
    api_hash=api_hash
)

# === Định nghĩa hàm xử lý tin nhắn ===
# Bot sẽ lắng nghe tin nhắn trong SOURCE_CHAT_ID
# và chỉ chuyển tiếp các tin nhắn chứa video hoặc ảnh.
@app.on_message(filters.chat(SOURCE_CHAT_ID) & (filters.video | filters.photo))
async def forward_media(client: Client, message: Message):
    """
    Hàm này sẽ được gọi khi có tin nhắn video hoặc ảnh mới trong nhóm/kênh nguồn.
    Nó sẽ sao chép tin nhắn đó đến nhóm/kênh đích với chú thích tùy chỉnh.
    """
    try:
        # In thông tin tin nhắn nhận được để tiện theo dõi log trên Render
        print(f"[{message.date}] Nhận được media từ {message.chat.title or message.chat.first_name} (ID: {message.chat.id}).")
        
        # Sao chép tin nhắn media đến nhóm/kênh đích
        await message.copy(TARGET_CHAT_ID, caption="cập nhật mới nhất")
        
        # In thông báo khi tin nhắn đã được chuyển tiếp thành công
        print(f"[{message.date}] Đã chuyển tiếp media (ID tin nhắn: {message.id}) đến {TARGET_CHAT_ID}.")
        
    except Exception as e:
        # Xử lý và in ra lỗi nếu có vấn đề trong quá trình chuyển tiếp
        print(f"Lỗi khi chuyển tiếp media từ {message.chat.id} (ID tin nhắn: {message.id}): {e}")

# === Hàm chạy chính của bot ===
async def main():
    """
    Hàm chính để khởi động, chạy và dừng bot.
    """
    print("Bot User đang khởi động...")
    
    # Bắt đầu phiên Pyrogram. Đây là lúc nó sẽ cố gắng đăng nhập
    # hoặc sử dụng file session đã có.
    await app.start() 
    
    # Lấy thông tin tài khoản đã đăng nhập để xác nhận bot đang hoạt động
    user_info = await app.get_me()
    print(f"Bot User đã đăng nhập với tên: {user_info.first_name} (@{user_info.username if user_info.username else 'No Username'})")
    print(f"ID của tài khoản bot: {user_info.id}") # In ID để tiện xác nhận

    print("Bot User đã sẵn sàng và đang lắng nghe tin nhắn...")
    
    # app.idle() sẽ giữ cho bot chạy liên tục cho đến khi bị dừng thủ công (Ctrl+C)
    # hoặc khi Render dừng dịch vụ.
    await idle() 
    
    # Dừng phiên Pyrogram khi bot kết thúc hoặc bị dừng
    await app.stop() 
    print("Bot User đã dừng.")

# Điểm khởi chạy chương trình
if __name__ == "__main__":
    # Chạy hàm main bất đồng bộ
    asyncio.run(main())

