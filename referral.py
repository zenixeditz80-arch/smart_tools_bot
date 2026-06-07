from config import BOT_USERNAME, DATABASE_NAME

from database import (
user_exists,
add_referral,
get_referral_count,
get_user
)

import sqlite3

def get_referral_link(user_id):
return (
f"https://t.me/"
f"{BOT_USERNAME}"
f"?start={user_id}"
)

def process_referral(
user_id,
referrer_id
):
try:

    if user_id == referrer_id:
        return False

    if not user_exists(referrer_id):
        return False

    if has_referral(user_id):
        return False

    add_referral(
        user_id,
        referrer_id
    )

    return True

except Exception as e:

    print(
        f"[REFERRAL ERROR] {e}"
    )

    return False

def has_referral(user_id):

try:

    with sqlite3.connect(
        DATABASE_NAME
    ) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM referrals
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return (
            cursor.fetchone()
            is not None
        )

except Exception:

    return False

def referral_count(user_id):

return get_referral_count(
    user_id
)

def get_referral_stats(user_id):

total = referral_count(
    user_id
)

return {
    "total_referrals": total,
    "reward_points": total
}

def get_reward_points(user_id):

return referral_count(
    user_id
)

def referral_text(user_id):

stats = get_referral_stats(
    user_id
)

link = get_referral_link(
    user_id
)

return f"""

👥 Referral System

🔗 Your Link:

{link}

📊 Statistics

Invites: {stats['total_referrals']}

🎁 Rewards: {stats['reward_points']}
"""

def get_leaderboard(
limit=10
):

try:

    with sqlite3.connect(
        DATABASE_NAME
    ) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                user_id,
                referrals
            FROM users
            ORDER BY referrals DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()

except Exception:

    return []

def leaderboard_text():

users = get_leaderboard()

if not users:
    return "No referral data."

text = "🏆 Referral Leaderboard\n\n"

for rank, user in enumerate(
    users,
    start=1
):

    text += (
        f"{rank}. "
        f"User {user[0]} "
        f"→ {user[1]} invites\n"
    )

return text

def eligible_for_reward(
user_id,
required=5
):
return (
referral_count(user_id)
>= required
)

def get_username(user_id):

user = get_user(
    user_id
)

if not user:
    return "Unknown"

return user[1]

def referral_bonus(user_id):

referrals = referral_count(
    user_id
)

if referrals >= 100:
    return "VIP"

if referrals >= 50:
    return "Premium"

if referrals >= 10:
    return "Fast Queue"

return "None"