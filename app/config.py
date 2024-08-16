import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()



# MongoDB setup
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]
users_collection = db['users']
conversations_collection = db['conversations']



# Telegram Bot Token 
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Twilio Account SID, Phone NUmber & Auth Token
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER') 


# SendGrid API Key 
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

# Meta Llama 3 API credentials 
LLAMA_API_KEY = os.environ.get('LLAMA_API_KEY')
LLAMA_API_ENDPOINT = os.environ.get('LLAMA_API_ENDPOINT')


