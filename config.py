TOKEN = "8411085201:AAGQ44CmWS0Be6baOLPV0Ib7ttvhIVRpNNc"

BOT_USERNAME = "SmartCelioToolsBot"

ADMIN_IDS = [
    8758830915
]

CHANNEL_USERNAME = "@CinemaHub_Channel"

CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"

DATABASE_NAME = "smarttools.db"

MAX_IMAGE_SIZE = 10 * 1024 * 1024
MAX_PDF_SIZE = 20 * 1024 * 1024

REFERRAL_REWARD = 1
START_BONUS_CONVERSIONS = 5

MAX_QUEUE_SIZE = 100
WORKER_THREADS = 3

PREMIUM_ENABLED = True
PREMIUM_FAST_QUEUE = True
PREMIUM_UNLIMITED_CONVERSIONS = True

TEMP_FOLDER = "data/temp"
LOG_FOLDER = "data/logs"
OUTPUT_FOLDER = "data/output"

ENABLE_LOGGING = True

ERROR_LOG_FILE = f"{LOG_FOLDER}/error.log"
ACTIVITY_LOG_FILE = f"{LOG_FOLDER}/activity.log"
CONVERSION_LOG_FILE = f"{LOG_FOLDER}/conversion.log"

REMOVE_BG_ENABLED = True

SUPPORTED_IMAGE_FORMATS = [
    "jpg",
    "jpeg",
    "png"
]

PDF_OUTPUT_FORMAT = "PNG"
PDF_DPI = 200

WELCOME_MESSAGE = """
🤖 Smart Tools Bot

/removebg
/pdf2img
/img2pdf
/referral
/help
"""

JOIN_REQUIRED_MESSAGE = (
    "❌ Please join our channel first to use this bot."
)

QUEUE_MESSAGE = (
    "⏳ Your request has been added to the queue."
)

PROCESSING_MESSAGE = (
    "🔄 Processing your request..."
)

DONE_MESSAGE = (
    "✅ Task completed successfully."
)
