from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from deep_translator import MyMemoryTranslator
from tools import *


BASE_PATH = "/home/aghil/Desktop/bot/deta"

chatbot = ChatBot(
    'MyBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=f'sqlite:///{BASE_PATH}/database.sqlite3',  
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ]
)

trainer = ChatterBotCorpusTrainer(chatbot)
# آموزش تمام کورپوس‌ها
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    
    "chatterbot.corpus.english.emotion", 
    "chatterbot.corpus.english.humor",
    "chatterbot.corpus.english.gossip",  
    
    "chatterbot.corpus.english.science",
    "chatterbot.corpus.english.history",
    "chatterbot.corpus.english.literature",
    "chatterbot.corpus.english.trivia",
    
    "chatterbot.corpus.english.computers",
    "chatterbot.corpus.english.ai",
    
    "chatterbot.corpus.english.movies", 
    "chatterbot.corpus.english.sports",
    "chatterbot.corpus.english.food",
    
    "chatterbot.corpus.english.money",
    "chatterbot.corpus.english.psychology"
)

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
# تست چت‌بات پس از آموزش
def test_bot():
    print("🤖 چت‌بات آماده است! سوال خود را بپرسید:")
    
    while True:
        try:
            user_input = input("شما: ")
            if user_input.lower() == 'exit':
                break
            response = chatbot.get_response(user_input)
            print(f"بات: {response}")
            
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

test_bot()