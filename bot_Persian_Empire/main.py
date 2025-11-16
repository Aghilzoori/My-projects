from Tools import *
from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update
from bot import run_chatbot
import asyncio
from chat_bat import generate_python_code

class Chat_Examinations:
    def __init__(self):
        pass
    async def Perform_operations(self, message):  
        
        Translation_fa_en = await asyncio.to_thread(Translator, message, "fa", "en")
        
        if Translation_fa_en is None:
            return "مشکل در اتصال اینترنت وجود دارد"
        
        is_request_result = is_request(Translation_fa_en)
        
        # if is_request_result:
        need_code_result = need_code(Translation_fa_en)
    
        if need_code_result:
            code_result = await asyncio.to_thread(generate_python_code, Translation_fa_en)
            return code_result or "کدی تولید نشد"
    
        needs_search_result = needs_internet_search_en_v4(Translation_fa_en)
        
        if needs_search_result:
            search_result = await asyncio.to_thread(run_search, message)
            return search_result or "نتیجه‌ای یافت نشد"
        
        Message_processing = await asyncio.to_thread(run_chatbot, Translation_fa_en)
        return Message_processing or "پاسخی دریافت نشد"
        
app = BotClient("توکن", timeout=120)

ID_user = {}

@app.on_update(filters.text, filters.private)
async def echo_private(client, update: Update):
    try:
        user_id = update.chat_id
        message_text = update.new_message.text
        
        
        if user_id not in ID_user:
            ID_user[user_id] = Chat_Examinations()
        
        get_class = ID_user[user_id]
        processing = await get_class.Perform_operations(message_text)
        
        # بررسی نهایی برای جلوگیری از None
        if processing is None:
            processing = "پاسخی دریافت نشد"
            
        await update.reply(processing)
        
    except Exception as e:
        await update.reply("متأسفانه مشکلی در پردازش پیام پیش آمد")

@app.on_update(filters.text, filters.group)
async def handle_group_messages(client, update: Update):
    try:
        if not update.new_message.reply_to_message_id:
            return
        
        user_id = getattr(update, 'author_guid', None) or getattr(update, 'chat_id', None)
        
        if not user_id:
            return
        
        message_text = update.new_message.text
        
        if user_id not in ID_user:
            ID_user[user_id] = Chat_Examinations()
        
        get_class = ID_user[user_id]
        processing = await get_class.Perform_operations(message_text)
        
        if processing is None:
            processing = "پاسخی دریافت نشد"
            
        await update.reply(processing)
        
    except Exception as e:
        print(f"❌ خطا در handle_group_messages: {e}")

if __name__ == "__main__":
    print("ربات در حال اجرا است - حالت چندکاربره همزمان (پشتیبانی از گروه و خصوصی)")
    app.run()
