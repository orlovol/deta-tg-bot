> [!WARNING]
> This repo is archived since deta.space is set to sunset on October 17, 2024.

# deta-tg-bot

Basic example of Telegram echo bot, using [FastAPI](https://fastapi.tiangolo.com/), [telegram webhooks](https://core.telegram.org/bots/webhooks) and deployed to [deta.space](https://deta.space/).

1. Get Telegram bot token from @BotFather
2. Deploy to deta with `space push` (no local dev)
3. Set token in app configuration on Deta
4. Invoke `/setup` once to set the webhook url
5. Write something to bot, get samething in return
