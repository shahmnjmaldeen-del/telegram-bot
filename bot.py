import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8872340033:AAHJ2JTgDxTmRK-gqY7fSiz_Bni2hior77s"
ADMIN_CHAT_ID = 8371477947

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 قسم شحن شدات ببجي (UC)", callback_data='pubg_prices')],
        [InlineKeyboardButton("⭐ اشتراكات تليغرام بريميوم", callback_data='telegram_subs')],
        [InlineKeyboardButton("🚀 خدمات تزويد السوشيال ميديا", callback_data='social_prices')],
        [InlineKeyboardButton("💳 طرق الدفع والتحويل المعتمدة", callback_data='payment_methods')],
        [InlineKeyboardButton("📥 طلب خدمة مخصصة أخرى", callback_data='custom_order')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = "مرحباً بك في المتجر الرقمي الآلي! 🛒🔥\nاختر القسم المطلوب من الأزرار أدناه:"
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'pubg_prices':
        await query.message.reply_text("🎮 أسعار شحن ببجي:\n• 60 شدة\n• 325 شدة\nأرسل الـ ID مع إشعار التحويل للطلب.")
    elif query.data == 'telegram_subs':
        await query.message.reply_text("⭐ اشتراكات تليغرام بريميوم:\nأرسل معرف حسابك للطلب.")
    elif query.data == 'social_prices':
        await query.message.reply_text("🚀 خدمات السوشيال ميديا:\nأرسل رابط الحساب للطلب.")
    elif query.data == 'payment_methods':
        await query.message.reply_text(
            "💳 **طرق الدفع المتوفرة:**\n\n"
            "1️⃣ **شام كاش (Sham Cash)** 🟢\n"
            "2️⃣ سيريتل كاش / إم تي إن كاش\n"
            "3️⃣ حوالات (الهرم / الفؤاد)\n"
            "4️⃣ عملات رقمية (USDT)\n\n"
            "📌 *للدفع عبر شام كاش أو أي طريقة أخرى، أرسل لنا رسالة هنا بعد إتمام التحويل مع صورة الإشعار أو رقم الحوالة للتنفيذ الفوري!*"
        )
    elif query.data == 'custom_order':
        await query.message.reply_text("📥 أرسل طلبك التفصيلي فوراً.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.effective_user.first_name
    user_handle = update.effective_user.username or "بدون معرف"
    user_id = update.effective_user.id
    
    await update.message.reply_text("✅ تم استلام طلبك بنجاح! جاري التوصيل والإشعار.")
    
    admin_message = f"🚨 طلب جديد من زبون!\n\nالاسم: {user_name}\nالمعرف: @{user_handle}\nID: {user_id}\n\nالطلب:\n{user_text}"
    
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except Exception as e:
        print(f"خطأ الإشعار: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 البوت يعمل الآن وتصلك الإشعارات للموبايل...")
    app.run_polling()
