import os
from bots.defaultBot import DefaultBot
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def gate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


class TGBot(DefaultBot):
    startChannels = []

    async def startBot(self):
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("gate", gate))

        application.run_polling(allowed_updates=Update.ALL_TYPES)

    def createBot(self):
        return