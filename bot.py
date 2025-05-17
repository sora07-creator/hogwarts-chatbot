import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import difflib

# Load data from the JSON file
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Function to find the best matching key
def get_answer(user_question):
    # Collect all possible answers (facts) into a list
    all_facts = []

    for key, value in data.items():
        if isinstance(value, str):
            all_facts.append(value)
        elif isinstance(value, dict):
            for subval in value.values():
                if isinstance(subval, str):
                    all_facts.append(subval)
                elif isinstance(subval, list):
                    # If list, extend facts
                    all_facts.extend(subval)
        elif isinstance(value, list):
            all_facts.extend(value)

    # Find closest matching fact to user question
    closest = difflib.get_close_matches(user_question.lower(), [fact.lower() for fact in all_facts], n=1, cutoff=0.4)

    if closest:
        return closest[0]  # Return the best matched fact (original text)
    else:
        return "Sorry, I don't know the answer to that."

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Ask me about the Hogwarts Summer School!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    answer = get_answer(user_question)
    await update.message.reply_text(answer)

# Main function to run the bot
def main():
    # Replace YOUR_BOT_TOKEN with your real token
    app = ApplicationBuilder().token("7714303155:AAG1geNamAgPgK0CKzL5qjMIJYUbcFP6hnA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
