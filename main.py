import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes,
    ConversationHandler, MessageHandler, filters
)

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

# Define conversation states
FEEDBACK = 1

user_db = set()
ADMIN_IDS = [651199698]  # Replace with actual Telegram user ID(s)

# Admin-only decorator
def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("🚫 You are not authorized.")
            return
        return await func(update, context)
    return wrapper

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_db.add(user_id)

    # Determine which message to reply to
    if update.message:
        message = update.message
    elif update.callback_query:
        message = update.callback_query.message
    else:
        return

    await message.reply_text(
        f"👋 Hello {update.effective_user.first_name}! Selamat datang ke bot CashPlantX. Pilih menu di bawah:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔧 Tools", callback_data="tools_menu"),
            InlineKeyboardButton("💬 Feedback", callback_data="feedback_start"),
            InlineKeyboardButton("ℹ️ Info", callback_data="info_menu"),
            InlineKeyboardButton("🚀 Start CashPlantX Bot", url="https://t.me/CashPlantX_bot?start=start")
        ], [
            InlineKeyboardButton("🛠 Admin Panel", callback_data="admin_panel")
        ]])
    )


# Show tools menu
async def tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(f"🛠️ {tool}", callback_data=f"tool_{tool}")]
        for tool in TOOLS
    ]
    keyboard += [
        [InlineKeyboardButton("❓ FAQ", callback_data="faq_menu")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ]
    await query.edit_message_text("📋 Pilih menu:", reply_markup=InlineKeyboardMarkup(keyboard))

# Show tool info
async def show_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tool_name = query.data.replace("tool_", "")
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

# Show FAQs
async def faq_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(f"❓ {question}", callback_data=f"faq_{i}")]
        for i, question in enumerate(FAQS)
    ]
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data="tools_menu")])
    await query.edit_message_text("📌 Pilih soalan yang anda ingin tahu:", reply_markup=InlineKeyboardMarkup(keyboard))

# FAQ answer
async def faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    index = int(query.data.replace("faq_", ""))
    question = list(FAQS.keys())[index]
    answer = FAQS[question]
    keyboard = [
        [InlineKeyboardButton("📚 FAQ lain", callback_data="faq_menu")],
        [InlineKeyboardButton("🔙 Menu Tools", callback_data="tools_menu")]
    ]
    await query.edit_message_text(f"*{question}*\n\n{answer}", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# Info menu
async def info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[
        InlineKeyboardButton("📨 Contact Support", url="https://t.me/CleopatraTheChartist"),
        InlineKeyboardButton("🌐 Website", url="https://cashplantx.com")
    ], [
        InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")
    ]]
    await query.edit_message_text("ℹ️ Info tambahan:", reply_markup=InlineKeyboardMarkup(keyboard))

# Feedback process
async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📝 Sila taip maklum balas anda sekarang:")
    return FEEDBACK

async def save_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback_text = update.message.text
    with open("feedback.txt", "a") as f:
        f.write(f"{update.effective_user.id}: {feedback_text}\n")
    await update.message.reply_text("🙏 Terima kasih atas maklum balas anda!")
    return ConversationHandler.END

# Admin panel
@admin_only
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📣 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📊 User Count", callback_data="admin_usercount")],
        [InlineKeyboardButton("📁 Export Feedback", callback_data="admin_feedback")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="main_menu")]
    ]
    await query.edit_message_text("🛠 Admin Panel:", reply_markup=InlineKeyboardMarkup(keyboard))

@admin_only
async def admin_usercount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"📊 Jumlah user: {len(user_db)}")

@admin_only
async def admin_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        with open("feedback.txt", "r") as f:
            feedback = f.read()
        await query.edit_message_text("📁 Semua Feedback:\n\n" + feedback[-3000:], parse_mode="Markdown")
    except FileNotFoundError:
        await query.edit_message_text("❌ Tiada feedback ditemui.")

# Admin broadcast
@admin_only
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    for user_id in user_db:
        try:
            await context.bot.send_message(chat_id=user_id, text=msg)
        except:
            pass
    await update.message.reply_text("✅ Broadcast sent.")

# Return to main menu
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# App setup
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))

    application.add_handler(CallbackQueryHandler(tools_menu, pattern="^tools_menu$"))
    application.add_handler(CallbackQueryHandler(show_tool, pattern="^tool_"))
    application.add_handler(CallbackQueryHandler(faq_menu, pattern="^faq_menu$"))
    application.add_handler(CallbackQueryHandler(faq_answer, pattern="^faq_\\d+$"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(feedback_start, pattern="^feedback_start$"))
    application.add_handler(CallbackQueryHandler(info_menu, pattern="^info_menu$"))

    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
    application.add_handler(CallbackQueryHandler(admin_usercount, pattern="^admin_usercount$"))
    application.add_handler(CallbackQueryHandler(admin_feedback, pattern="^admin_feedback$"))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)],
        states={FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)]},
        fallbacks=[]
    )
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
