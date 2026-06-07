import os
import shutil
import zipfile
import telebot

from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    TOKEN,
    CHANNEL_USERNAME,
    TEMP_FOLDER,
    OUTPUT_FOLDER,
    MAX_IMAGE_SIZE,
    MAX_PDF_SIZE
)

from database import (
    add_user,
    get_total_users,
    add_conversion,
    is_banned
)

from referral import (
    process_referral,
    get_referral_link,
    referral_text
)

from admin import (
    is_admin,
    broadcast_handler,
    stats_handler
)

from join_checker import (
    check_join
)

from removebg import (
    remove_background
)

from converter import (
    pdf_to_images,
    image_to_pdf
)

bot = telebot.TeleBot(
    TOKEN,
    parse_mode="HTML"
)

os.makedirs(
    TEMP_FOLDER,
    exist_ok=True
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

user_states = {}

REMOVE_BG = "REMOVE_BG"
PDF_TO_IMG = "PDF_TO_IMG"
IMG_TO_PDF = "IMG_TO_PDF"

def clear_file(path):

    try:

        if os.path.exists(path):
            os.remove(path)

    except Exception:
        pass


def clear_folder(folder):

    try:

        if os.path.exists(folder):
            shutil.rmtree(folder)

        os.makedirs(
            folder,
            exist_ok=True
        )

    except Exception:
        pass


def create_zip(
    folder,
    zip_path
):

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for root, dirs, files in os.walk(folder):

            for file in files:

                full_path = os.path.join(
                    root,
                    file
                )

                zipf.write(
                    full_path,
                    file
                )

    return zip_path
    
@bot.message_handler(commands=["start"])
def start(message):

    user_id = message.from_user.id
    username = message.from_user.username or "None"

    add_user(
        user_id,
        username
    )

    if is_banned(user_id):

        bot.send_message(
            message.chat.id,
            "🚫 You are banned."
        )

        return

    args = message.text.split()

    if len(args) > 1:

        try:

            referrer_id = int(
                args[1]
            )

            process_referral(
                user_id,
                referrer_id
            )

        except Exception as e:

            print(
                f"Referral Error: {e}"
            )

    if not check_join(
        bot,
        user_id
    ):

        markup = InlineKeyboardMarkup()

        markup.add(
            InlineKeyboardButton(
                "📢 Join Channel",
                url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
            )
        )

        bot.send_message(
            message.chat.id,
            """
❌ Please join our channel first.

After joining,
send /start again.
""",
            reply_markup=markup
        )

        return

    bot.send_message(
        message.chat.id,
        """
🤖 <b>Smart Tools Bot</b>

Available Commands

/removebg
/pdf2img
/img2pdf
/referral
/help
"""
    )


@bot.message_handler(commands=["help"])
def help_command(message):

    if not check_join(
        bot,
        message.from_user.id
    ):
        return

    bot.send_message(
        message.chat.id,
        """
📚 Smart Tools Bot Help

🖼 /removebg
Remove image background

📄 /pdf2img
Convert PDF to images

🖼 /img2pdf
Convert image to PDF

👥 /referral
Referral system

📊 /stats
Admin only
"""
    )


@bot.message_handler(commands=["referral"])
def referral_command(message):

    if not check_join(
        bot,
        message.from_user.id
    ):
        return

    bot.send_message(
        message.chat.id,
        referral_text(
            message.from_user.id
        )
    )


@bot.message_handler(commands=["removebg"])
def removebg_command(message):

    if not check_join(
        bot,
        message.from_user.id
    ):
        return

    user_states[
        message.from_user.id
    ] = REMOVE_BG

    bot.send_message(
        message.chat.id,
        """
🖼 Send an image.

Background will be removed
automatically.
"""
    )


@bot.message_handler(commands=["pdf2img"])
def pdf2img_command(message):

    if not check_join(
        bot,
        message.from_user.id
    ):
        return

    user_states[
        message.from_user.id
    ] = PDF_TO_IMG

    bot.send_message(
        message.chat.id,
        """
📄 Send PDF file.

All pages will be converted
to PNG images and packed
into ZIP.
"""
    )


@bot.message_handler(commands=["img2pdf"])
def img2pdf_command(message):

    if not check_join(
        bot,
        message.from_user.id
    ):
        return

    user_states[
        message.from_user.id
    ] = IMG_TO_PDF

    bot.send_message(
        message.chat.id,
        """
🖼 Send image.

Image will be converted
to PDF.
"""
    )
    
@bot.message_handler(commands=["stats"])
def stats_command(message):

    user_id = message.from_user.id

    if not is_admin(user_id):

        bot.reply_to(
            message,
            "❌ Admin only."
        )

        return

    total_users = get_total_users()

    stats_handler(
        bot,
        message,
        total_users
    )


@bot.message_handler(commands=["broadcast"])
def broadcast_command(message):

    user_id = message.from_user.id

    if not is_admin(user_id):

        bot.reply_to(
            message,
            "❌ Admin only."
        )

        return

    broadcast_handler(
        bot,
        message
    )


@bot.message_handler(commands=["admin"])
def admin_command(message):

    user_id = message.from_user.id

    if not is_admin(user_id):

        bot.reply_to(
            message,
            "❌ Admin only."
        )

        return

    total_users = get_total_users()

    bot.send_message(
        message.chat.id,
        f"""
🛠 Smart Tools Admin Panel

👥 Users: {total_users}

Commands:

/stats
/broadcast TEXT
"""
    )
    
@bot.message_handler(content_types=["photo"])
def photo_handler(message):

    user_id = message.from_user.id

    if not check_join(
        bot,
        user_id
    ):
        return

    state = user_states.get(
        user_id
    )

    if not state:

        bot.reply_to(
            message,
            "❓ Choose a command first."
        )

        return

    try:

        photo = message.photo[-1]

        file_info = bot.get_file(
            photo.file_id
        )

        if file_info.file_size:

            if file_info.file_size > MAX_IMAGE_SIZE:

                bot.reply_to(
                    message,
                    "❌ Image too large."
                )

                return

        bot.send_message(
            message.chat.id,
            "⏳ Processing..."
        )

        temp_input = os.path.join(
            TEMP_FOLDER,
            f"{user_id}.jpg"
        )

        downloaded = bot.download_file(
            file_info.file_path
        )

        with open(
            temp_input,
            "wb"
        ) as f:

            f.write(
                downloaded
            )

        if state == REMOVE_BG:

            output_png = os.path.join(
                OUTPUT_FOLDER,
                f"{user_id}_nobg.png"
            )

            remove_background(
                temp_input,
                output_png
            )

            with open(
                output_png,
                "rb"
            ) as photo_file:

                bot.send_document(
                    message.chat.id,
                    photo_file,
                    caption="✅ Background Removed"
                )

            add_conversion(
                user_id,
                "REMOVE_BG"
            )

            clear_file(
                output_png
            )

        elif state == IMG_TO_PDF:

            output_pdf = os.path.join(
                OUTPUT_FOLDER,
                f"{user_id}.pdf"
            )

            image_to_pdf(
                temp_input,
                output_pdf
            )

            with open(
                output_pdf,
                "rb"
            ) as pdf_file:

                bot.send_document(
                    message.chat.id,
                    pdf_file,
                    caption="✅ PDF Created"
                )

            add_conversion(
                user_id,
                "IMG_TO_PDF"
            )

            clear_file(
                output_pdf
            )

        clear_file(
            temp_input
        )

        user_states.pop(
            user_id,
            None
        )

    except Exception as e:

        bot.reply_to(
            message,
            f"❌ Error:\n{e}"
        )

        user_states.pop(
            user_id,
            None
        )
        
@bot.message_handler(content_types=["document"])
def document_handler(message):

    user_id = message.from_user.id

    if not check_join(
        bot,
        user_id
    ):
        return

    state = user_states.get(
        user_id
    )

    if state != PDF_TO_IMG:

        bot.reply_to(
            message,
            "❓ Use /pdf2img first."
        )

        return

    try:

        file_name = (
            message.document.file_name or ""
        ).lower()

        if not file_name.endswith(
            ".pdf"
        ):

            bot.reply_to(
                message,
                "❌ PDF file only."
            )

            return

        if message.document.file_size:

            if (
                message.document.file_size
                > MAX_PDF_SIZE
            ):

                bot.reply_to(
                    message,
                    "❌ PDF too large."
                )

                return

        bot.send_message(
            message.chat.id,
            "⏳ Converting PDF..."
        )

        temp_pdf = os.path.join(
            TEMP_FOLDER,
            f"{user_id}.pdf"
        )

        output_dir = os.path.join(
            OUTPUT_FOLDER,
            str(user_id)
        )

        zip_file = os.path.join(
            OUTPUT_FOLDER,
            f"{user_id}_images.zip"
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        file_info = bot.get_file(
            message.document.file_id
        )

        downloaded = bot.download_file(
            file_info.file_path
        )

        with open(
            temp_pdf,
            "wb"
        ) as f:

            f.write(
                downloaded
            )

        pdf_to_images(
            temp_pdf,
            output_dir
        )

        create_zip(
            output_dir,
            zip_file
        )

        with open(
            zip_file,
            "rb"
        ) as zip_doc:

            bot.send_document(
                message.chat.id,
                zip_doc,
                caption="✅ PDF Converted"
            )

        add_conversion(
            user_id,
            "PDF_TO_IMG"
        )

        clear_file(
            temp_pdf
        )

        clear_file(
            zip_file
        )

        clear_folder(
            output_dir
        )

        user_states.pop(
            user_id,
            None
        )

    except Exception as e:

        bot.reply_to(
            message,
            f"❌ Error:\n{e}"
        )

        user_states.pop(
            user_id,
            None
        )
        
@bot.message_handler(func=lambda message: True)
def unknown_handler(message):

    bot.reply_to(
        message,
        """
❓ Unknown command.

Available Commands:

/removebg
/pdf2img
/img2pdf
/referral
/help
"""
    )


print(
    "🤖 Smart Tools Bot Started..."
)

while True:

    try:

        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60,
            skip_pending=True
        )

    except Exception as e:

        print(
            f"[BOT ERROR] {e}"
        )

        import time

        time.sleep(
            5
        )