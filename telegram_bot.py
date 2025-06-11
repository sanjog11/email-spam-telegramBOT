from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pickle
import os
# Load your trained model and vectorizer
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Replace with your actual bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("👋 Hello! Send me any email text and I’ll tell you if it's SPAM or NOT.")

def detect_spam(update, context):
    text = update.message.text
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0]
    if prediction == 1:
        result = "✅ This looks like a **NOT SPAM** email."
    else:
        result = "🚨 This looks like a **SPAM** email."
    update.message.reply_text(result)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_spam))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
