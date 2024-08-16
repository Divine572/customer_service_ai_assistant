from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from datetime import datetime, timezone


from models import User, Message, Conversation


from config import (
        TELEGRAM_BOT_TOKEN, 
        TWILIO_ACCOUNT_SID, 
        TWILIO_AUTH_TOKEN,
        LLAMA_API_KEY, 
        LLAMA_API_ENDPOINT, 
        users_collection, 
        conversations_collection
    )

from utils import get_ai_response, get_current_utc_time



commands = [
    BotCommand("start", "Start the Customer Support Assistant bot"),
    BotCommand("help", "Get help"),
]



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    
    
    user_data = User(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code
    )
    
    users_collection.update_one({'telegram_id': user.id}, {'$set': user_data.model_dump()}, upsert=True)
    await update.message.reply_text('Welcome to our Customer Service Bot! How can I help you today?')



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
    Here are the available commands:
    /start - Start the bot
    /help - Show this help message
    
    You can also simply type your question or concern, and I'll do my best to assist you!
    """
    await update.message.reply_text(help_text)



async def set_commands(application):
    await application.bot.set_my_commands(commands)



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_message = update.message.text
    current_utc_time = get_current_utc_time()

    # Update last interaction time
    users_collection.update_one({'telegram_id': user.id}, {'$set': {'last_interaction': current_utc_time}})

    # Get or create conversation
    user_id_filter = {'user_id': user.id, 'end_time': None}
    conversation = conversations_collection.find_one(user_id_filter)

    if not conversation:
        new_conversation = Conversation(user_id=user.id)
        result = conversations_collection.insert_one(new_conversation.model_dump(by_alias=True, exclude={'id'}))
        conversation = conversations_collection.find_one({'_id': result.inserted_id})


    # Add user message to conversation (convert to dictionary)
    user_message_dict = {
        "content": user_message,
        "timestamp": current_utc_time,
        "is_from_user": True,
    }
    conversation["messages"].append(user_message_dict)

    # Get AI response
    ai_response = await get_ai_response(user_message)

    # Add AI response to conversation (convert to dictionary)
    ai_message_dict = {
        "content": ai_response,
        "timestamp": current_utc_time,
        "is_from_user": False,
    }
    
    conversation["messages"].append(ai_message_dict)

    # Update conversation in database
    conversations_collection.update_one(
        {'_id': conversation["_id"]},
        {'$set': {
            'messages': conversation["messages"],
            'last_updated': current_utc_time
        }}
    )

    await update.message.reply_text(ai_response)
    
    
    

    
    
def main() -> None:
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()


    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    

    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    
    
if __name__ == "__main__":
    print("Bot is running...")
    
    main()