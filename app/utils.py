from datetime import datetime, timezone



async def get_ai_response(message: str) -> str:
    
    return f"I understood your message: {message}. How can I assist you further?"


def get_current_utc_time():
  return datetime.now(timezone.utc)
