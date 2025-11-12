from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update
from login_ver import Login

app = BotClient("")

user_sessions = {}

@app.on_update(filters.text, filters.private)
async def echo(client, update: Update):
    user_id = update.chat_id
    message_text = update.new_message.text
    
    if user_id not in user_sessions:
        user_sessions[user_id] = Login()
    
    login_session = user_sessions[user_id]
    result = login_session.process_message(message_text)  
    
    await update.reply(result)

if __name__ == "__main__":
    print("ربات در حال اجرا است")
    app.run()