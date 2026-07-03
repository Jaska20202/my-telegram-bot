from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import csv
import os

# --- ALWAYS USE SCRIPT FOLDER ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "bot_log.csv")

# --- AUTO-CREATE CSV IF MISSING ---
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("timestamp,user_id,username,first_name,action,text\n")

# --- BOT TOKEN ---
TOKEN = os.getenv("BOT_TOKEN")   # taken from Render environment
BOT_USERNAME = "@your_bot_username_here"   # optional for group logic


# --- LOGGING FUNCTION ---
def log_user_action(update: Update, action: str):
    try:
        user = update.message.from_user
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                user.id,
                user.username,
                user.first_name,
                action,
                update.message.text
            ])
    except Exception as e:
        print("Logging error:", e)


# --- COMMANDS ---
async def boshlamoq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Raxmat! Meni ishlatganingiz uchun. Sizning qaydlaringizni ro'yhatga olaman."
    )
    log_user_action(update, "Pressed /boshlamoq")


async def asosiy_darsga_qatnashdim_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Raxmat asosiy darsga qatnashganingiz uchun. Kelasi asosiy darslarimizgacha Allahga omonatsiz!"
    )
    log_user_action(update, "Pressed /asosiy_darsga_qatnashdim")


async def asosiy_dars_topshirdim_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Juda minaddormiz. Ilmingiz bundanda ziyoda bo'lsin."
    )
    log_user_action(update, "Pressed /asosiy_dars_topshirdim")


async def konspekt_qildim_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Yozgan qo'llaringiz dard ko'rmasin! Bu qaydnomalar sizga uzoq yillar xizmat qiladi. Endi konspektingizni rasmga olib joylashtiring."
    )
    log_user_action(update, "Pressed /konspekt_qildim")


async def boshqa_savolim_bor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Savolingizni yozing, Allah qodir qilguncha javob beramiz."
    )
    log_user_action(update, "Pressed /boshqa_savolim_bor")


# --- TEXT RESPONSE LOGIC ---
def handle_response(text: str) -> str:
    processed = text.lower()

    if ("assalomu aleykum" in processed or
        "assalomu aleykum wa rahmatullohi wa barakatuhi" in processed or
        "assalomu aleykum va rahmatullohi va barakatuh" in processed):
        return "Wa aleykum Assalom Wa Rahmatullohi Wa Barakatuhi"

    if ("allah rozi bo'lsin sizdan" in processed or
        "allah rozi bo'lsin" in processed):
        return "Allah jumlamizdan rozi bo'lsin!"
    
    if ("raxmat" in processed or
        "sog' bo'ling" in processed):
        return "JazakAllah Khayr! Sizga ham sog'liq va baraka tilayman!"
    
    if ("yaxshimiz?" in processed or
        "qalisiz" in processed):
        return "Alhamdullilah, yaxshimiz. O'zingiz omonmisiz? Sizni sog'liq va baraka bilan ko'rishdan xursandman!"

    return "Savolingizga tushunmadim. Guruhga murojat qiling."


# --- MESSAGE HANDLER ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f"User({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type in ["group", "supergroup"]:
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)
    log_user_action(update, "Sent message")


# --- ERROR HANDLER ---
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# --- MAIN ---
if __name__ == "__main__":
    print("Botni boshlash...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("boshlamoq", boshlamoq_command))
    app.add_handler(CommandHandler("asosiy_darsga_qatnashdim", asosiy_darsga_qatnashdim_command))
    app.add_handler(CommandHandler("asosiy_dars_topshirdim", asosiy_dars_topshirdim_command))
    app.add_handler(CommandHandler("konspekt_qildim", konspekt_qildim_command))
    app.add_handler(CommandHandler("boshqa_savolim_bor", boshqa_savolim_bor_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling()
