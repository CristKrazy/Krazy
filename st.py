import logging
import os
import zipfile
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Thiết lập logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Đường dẫn tới thư mục lưu trữ sticker
STICKER_FOLDER = "stickers"

# Callback cho lệnh /get
def get_stickers(update: Update, context: CallbackContext):
    # Lấy đường dẫn sticker từ lệnh
    sticker_url = context.args[0]

    # Tạo thư mục nếu nó chưa tồn tại
    os.makedirs(STICKER_FOLDER, exist_ok=True)

    # Tải sticker về
    response = requests.get(sticker_url)
    if response.status_code == 200:
        sticker_filename = os.path.join(STICKER_FOLDER, "sticker.webp")
        with open(sticker_filename, 'wb') as sticker_file:
            sticker_file.write(response.content)
        
        # Nén sticker thành file .zip
        with zipfile.ZipFile('stickers.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(sticker_filename, os.path.basename(sticker_filename))

        # Gửi file .zip cho người dùng
        update.message.reply_document(document=open('stickers.zip', 'rb'))
    else:
        update.message.reply_text("Không thể tải sticker từ đường dẫn này.")

# Hàm main
def main():
    # Khởi tạo Updater với token của bot
    updater = Updater(token="6100654723:AAEnplbnamn60BjZh7FSj0pKRE2X3HYfq-Y", use_context=True)

    # Lấy dispatcher để đăng ký các handler
    dispatcher = updater.dispatcher

    # Đăng ký handler cho lệnh /get
    dispatcher.add_handler(CommandHandler("get", get_stickers, pass_args=True))

    # Bắt đầu chạy bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
