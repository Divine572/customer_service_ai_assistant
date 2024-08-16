
# AI-Powered Customer Service Assistant

## Overview

This project implements an AI-powered customer service assistant using Telegram as the user interface, Meta Llama 3 for natural language processing, and Twilio SendGrid for SMS notifications. The bot is designed to understand and respond to customer queries, provide solutions, and escalate issues to human agents when necessary.

## Features

- Telegram bot interface for user interactions
- AI-powered responses using Meta Llama 3
- SMS notifications via Twilio SendGrid
- Escalation to human agents for complex queries
- Easy-to-use Python-based implementation

## Prerequisites

- Python 3.7+
- Telegram Bot Token
- Meta Llama 3 API access (or similar AI model)
- Twilio SendGrid API key

## Installation

1. Clone the repository:
   ```
    git clone https://github.com/Divine572/ai-customer-service-assistant.git
    cd ai-customer-service-assistant     
   ```

2. Install required packages:

   ```
    pip install -r requirements.txt
   ```

3. Set up environment variables:

   Create a `.env` file in the project root and add the following:
   ```
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    SENDGRID_API_KEY=your_sendgrid_api_key
    META_LLAMA_API_KEY=your_meta_llama_api_key   
   ```

## Usage

1. Run the bot:

    ```
        python3 app/bot.py
    ```

2. Open Telegram and start a conversation with your bot.

3. Send messages to interact with the AI-powered assistant.

## Configuration

- Adjust the AI model parameters in `get_ai_response()` function.
- Modify escalation thresholds in the message handling logic.
- Customize SMS notification templates in the Twilio SendGrid integration.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.



## Acknowledgments

- Telegram Bot API
- Meta Llama 3
- Twilio SendGrid
- Python Telegram Bot library

