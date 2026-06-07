import os
import threading
from datetime import datetime

LOG_DIR = "data/logs"

ERROR_LOG = os.path.join(
    LOG_DIR,
    "error.log"
)

ACTIVITY_LOG = os.path.join(
    LOG_DIR,
    "activity.log"
)

CONVERSION_LOG = os.path.join(
    LOG_DIR,
    "conversion.log"
)

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

log_lock = threading.Lock()


def timestamp():
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def write_log(
    file_path,
    message
):
    try:

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        with log_lock:

            with open(
                file_path,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(
                    f"[{timestamp()}] {message}\n"
                )

    except Exception as e:

        print(
            f"[LOGGER ERROR] {e}"
        )


def log_error(error):
    write_log(
        ERROR_LOG,
        str(error)
    )


def log_activity(
    user_id,
    action
):
    write_log(
        ACTIVITY_LOG,
        f"User: {user_id} | {action}"
    )


def log_conversion(
    user_id,
    conversion_type
):
    write_log(
        CONVERSION_LOG,
        f"User: {user_id} | Type: {conversion_type}"
    )


def log_broadcast(
    admin_id,
    sent_count
):
    write_log(
        ACTIVITY_LOG,
        f"Broadcast | Admin: {admin_id} | Sent: {sent_count}"
    )


def log_ban(
    admin_id,
    user_id
):
    write_log(
        ACTIVITY_LOG,
        f"BAN | Admin: {admin_id} | User: {user_id}"
    )


def log_unban(
    admin_id,
    user_id
):
    write_log(
        ACTIVITY_LOG,
        f"UNBAN | Admin: {admin_id} | User: {user_id}"
    )


def read_log(
    file_path,
    limit=100
):
    try:

        if not os.path.exists(
            file_path
        ):
            return []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            lines = f.readlines()

        return lines[-limit:]

    except Exception:

        return []


def clear_log(
    file_path
):
    try:

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ):
            pass

        return True

    except Exception:

        return False


def get_log_size(
    file_path
):
    try:

        return (
            os.path.getsize(file_path)
            if os.path.exists(file_path)
            else 0
        )

    except Exception:

        return 0


def get_log_info():
    return {
        "error_log_size":
            get_log_size(ERROR_LOG),

        "activity_log_size":
            get_log_size(ACTIVITY_LOG),

        "conversion_log_size":
            get_log_size(CONVERSION_LOG)
    }