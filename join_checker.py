from config import CHANNEL_USERNAME


def get_member(bot, user_id):
    try:
        return bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )
    except Exception as e:
        print(
            f"[JOIN CHECK ERROR] {e}"
        )
        return None


def check_join(bot, user_id):
    member = get_member(
        bot,
        user_id
    )

    if not member:
        return False

    return member.status in (
        "member",
        "administrator",
        "creator",
        "owner"
    )


def require_join(
    bot,
    message
):
    return check_join(
        bot,
        message.from_user.id
    )


def get_member_status(
    bot,
    user_id
):
    member = get_member(
        bot,
        user_id
    )

    if member:
        return member.status

    return None


def is_channel_admin(
    bot,
    user_id
):
    member = get_member(
        bot,
        user_id
    )

    if not member:
        return False

    return member.status in (
        "administrator",
        "creator",
        "owner"
    )


def can_use_bot(
    bot,
    user_id
):
    return check_join(
        bot,
        user_id
    )