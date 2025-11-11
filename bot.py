from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement

def run_chatbot(message):
    # ساخت چت‌بات
    chatbot = ChatBot(
        'Persian_Empire',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

    # آموزش چت‌بات
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")


    response = chatbot.get_response(message)

    def Adding_text(test, answer):
        """Adding text to the database"""
        #افزودن یک متن و جواب ان در دیتابیس بات
        chatbot.storage.create(
            Statement(text="سلام"),
            [Statement(text="سلام! خوش اومدی")]
        )
    return response