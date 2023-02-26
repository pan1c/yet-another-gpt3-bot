# yet-another-gpt3-bot

Telegram bot that allows you to speak with gpt3 model.
--

## Usage

###### Pure python
```
 pip install -r requirements.txt
 TELEGRAM_BOT_TOKEN=<your tg token> OPENAI_API_KEY=<your open AI token> python3 gpt3_bot.py
```

###### Docker
- create file _secrets.env_ with your secrets:
```
cat secrets.env
TELEGRAM_BOT_TOKEN=<your tg token>
OPENAI_API_KEY=<your open AI token>
```
- run docker compose up command
```
docker compose up
```

