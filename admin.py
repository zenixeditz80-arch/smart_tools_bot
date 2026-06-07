from config import ADMIN_IDS
from database import (
    get_all_users,
    ban_user_db,
    unban_user_db,
    get_user_info
)

def is_admin(user_id):
    return user_id in ADMIN_IDS

def stats_handler(bot, message, total_users):
    text = f"""
📊 Smart Tools Bot Statistics

👥 Total Users: {total_users}

🤖 Bot Status: Online
"""
    bot.send_message(message.chat.id, text)

def broadcast_handler(bot, message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        bot.reply_to(
            message,
            "Usage:\n\n/broadcast Your message here"
        )
        return

    broadcast_text = args[1].strip()

    if not broadcast_text:
        bot.reply_to(
            message,
            "❌ Broadcast message cannot be empty."
        )
        return

    users = get_all_users()

    sent = 0
    failed = 0

    for user in users:
        try:
            user_id = user[0] if isinstance(user, tuple) else user

            bot.send_message(
                user_id,
                broadcast_text
            )

            sent += 1

        except Exception as e:
            print(
                f"Broadcast Error: {e}"
            )
            failed += 1

    bot.send_message(
        message.chat.id,
        f"""
📢 Broadcast Finished

✅ Sent: {sent}
❌ Failed: {failed}
"""
    )

def ban_user(user_id):
    return ban_user_db(user_id)

def unban_user(user_id):
    return unban_user_db(user_id)

def user_info(user_id):
    return get_user_info(user_id)