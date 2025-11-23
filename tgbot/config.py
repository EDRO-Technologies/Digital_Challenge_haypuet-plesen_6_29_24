import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_URL = os.getenv('API_URL')
API_TOKEN = os.getenv('API_TOKEN')
EVENTS_API_URL = f"{API_URL}/events"
NOTIFICATIONS_API_URL = f"{API_URL}/users?need_notification=true"