import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your bot token
TOKEN = "8049795725:AAHOhnqgpq3GsFYqpuh8Ro7IuvXOBx5zekM"

# Define tools and FAQs
TOOLS = ["CashPlantX"]
FAQS = {
    "Apa itu CashPlantX?": "CashPlantX ialah sistem AI + EA yang auto-trade Gold (XAUUSD) untuk bantu anda grow akaun secara konsisten.",
    "Perlu ada pengalaman trading?": "Tak perlu. Sistem ini sesuai untuk beginner, busy trader, atau yang trauma dengan MC.",
    "Berapa modal minimum?": "Modal minimum yang disarankan ialah $100 (lebih tinggi = lebih selamat).",
    "Boleh withdraw profit?": "Ya! Akaun milik anda sepenuhnya, boleh withdraw bila-bila masa.",
    "Siapa yang setup?": "Team CashPlantX akan uruskan semua setup dari A-Z untuk anda."
}


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! Selamat datang ke bot CashPlantX. Pilih menu di bawah:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔧 Tools", callback_data="tools_menu")]])
    )


# Show tools menu with inline buttons
async def tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=tool, callback_data=f"tool_{tool}")]
        for tool in TOOLS
    ]
    keyboard.append([InlineKeyboardButton("❓ FAQ", callback_data="faq_menu")])

    await query.edit_message_text("Pilih menu:", reply_markup=InlineKeyboardMarkup(keyboard))


# Handle tool selection (e.g. CashPlantX)
async def show_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tool_name = query.data.replace("tool_", "")

    # Tool response
    if tool_name == "CashPlantX":
        response = (
            "💎 *CashPlantX - Mesin Cetak USD Dengan AI + EA*\n\n"
            "Ramai Trader sangkut sebab:\n"
            "❌ Tak sempat tengok chart\n"
            "❌ Tak tahu bila nak entry\n"
            "❌ Emosi tak stabil bila floating\n\n"
            "Dengan CashPlantX:\n"
            "✅ Auto-trade Gold (XAUUSD)\n"
            "✅ Sesuai untuk busy / newbie / trauma trader\n"
            "✅ Team setup dari A-Z\n"
            "✅ Boleh monitor dari mana-mana\n\n"
            "[📝 Daftar Sekarang](https://t.me/CleopatraTheChartist)"
        )
        await query.edit_message_text(response, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        await query.edit_message_text(f"Tool *{tool_name}* belum disediakan.", parse_mode="Markdown")


# Show list of FAQs
async def faq_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text=question, callback_data=f"faq_{i}")]
        for i, question in enumerate(FAQS)
    ]
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="tools_back")])
    await query.edit_message_text("Pilih soalan yang anda ingin tahu:", reply_markup=InlineKeyboardMarkup(keyboard))


# Show FAQ answer
async def faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data.replace("faq_", ""))
    question = list(FAQS.keys())[index]
    answer = FAQS[question]
    keyboard = [
        [InlineKeyboardButton("❓ FAQ lain", callback_data="faq_menu")],
        [InlineKeyboardButton("🔙 Menu Tools", callback_data="tools_back")]
    ]
    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown",
                                  reply_markup=InlineKeyboardMarkup(keyboard))


# Handle going back to tools menu
async def back_to_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await tools_menu(update, context)


# Main function to setup handlers
def main():
    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add command and callback query handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(tools_menu, pattern="^tools_menu$"))
    application.add_handler(CallbackQueryHandler(show_tool, pattern="^tool_"))
    application.add_handler(CallbackQueryHandler(faq_menu, pattern="^faq_menu$"))
    application.add_handler(CallbackQueryHandler(faq_answer, pattern="^faq_\\d+$"))
    application.add_handler(CallbackQueryHandler(back_to_tools, pattern="^tools_back$"))

    # Start polling
    application.run_polling()


if __name__ == "__main__":
    main()

ADMIN_IDS = [123456789]  # Replace with actual Telegram user ID(s)

def admin_only(func):
    def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            return update.message.reply_text("You are not authorized.")
        return func(update, context)
    return wrapper

@admin_only
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    for user_id in user_db:  # assumes you are tracking users
        try:
            await context.bot.send_message(chat_id=user_id, text=msg)
        except:
            pass
    await update.message.reply_text("Broadcast sent.")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send your feedback now:")
    return FEEDBACK  # Use ConversationHandler to handle this flow

async def save_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback_text = update.message.text
    with open("feedback.txt", "a") as f:
        f.write(f"{update.effective_user.id}: {feedback_text}\n")
    await update.message.reply_text("Thanks for your feedback!")
    return ConversationHandler.END

user_db = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_db.add(user_id)
    await update.message.reply_text("Welcome to CPXBot!")

