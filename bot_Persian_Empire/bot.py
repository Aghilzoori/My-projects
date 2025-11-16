from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from deep_translator import MyMemoryTranslator
from Tools import *


# چت‌بات اصلی
chatbot = ChatBot(
    'Persian_Empire',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

def create_or_load_bot(name="Persian_Empire", storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri="sqlite:///database.sqlite3"):
    bot = ChatBot(
        name,
        storage_adapter=storage_adapter,
        database_uri=database_uri,  # اصلاح: database -> database_uri
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.90
            }
        ]
    )
    return bot

def translate_text(text, source_lang='english', target_lang='persian'):
    """ترجمه متن"""
    if not text or text.strip() == "":
        return ""
    try:
        translator = MyMemoryTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except:
        return text
def train_bot(bot, conversation_pairs):
    """
    conversation_pairs: لیست جفت‌های (سوال, پاسخ)
    مثال: [("سلام", "سلام! خوبی؟"), ("حالت چطوره؟", "خوبم، تو چطوری؟")]
    """
    trainer = ListTrainer(bot)
    for pair in conversation_pairs:
        question, answer = pair
        trainer.train([question, answer])

def run_chatbot(message):
    try:
    # پاسخ معمولی با ChatterBot
        message_en = Translator(message, "fa", "en")
        response_en = chatbot.get_response(message_en)
        # ترجمه پاسخ به فارسی
        response_fa = translate_text(str(response_en))
        return response_fa if response_fa else str(response_en)
            
    except Exception as e:
        return "در پردازش سوال مشکلی پیش آمد. لطفاً دوباره تلاش کنید."

# تابع کمکی برای تشخیص فارسی
def contains_persian(text):
    """تشخیص وجود حروف فارسی در متن"""
    persian_chars = set('ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی')
    return any(char in persian_chars for char in text)
