from deep_translator import GoogleTranslator, MyMemoryTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from search_link import *
from get_Information_link import *
import re



def Translator(text, so, ta):
    translated = GoogleTranslator(source=so, target=ta).translate(text)
    return translated

def clean_text(text):
    try:
        return ' '.join(text.split()).strip()
    except:
        return text

def translate_text(text, source_lang='en', target_lang='fa'):
    """
    ترجمه متن با استفاده از MyMemoryTranslator
    متن را پاکسازی می‌کند و ترجمه می‌کند.
    
    پارامترها:
    text: str -> متن ورودی
    source_lang: str -> زبان متن ورودی (default='en')
    target_lang: str -> زبان مقصد (default='fa')
    """
    if not text or text.strip() == "":
        return ""  

    # پاکسازی متن: حذف فاصله‌های اضافی و کاراکترهای نامرئی
    cleaned_text = ' '.join(text.split()).strip()
    
    try:
        translator = MyMemoryTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(cleaned_text)
        return translated_text
    except Exception as e:
        return f"خطا در ترجمه: {e}"


def extract_related_part(question, previous_answer):
    """
    استخراج بخش مرتبط از پاسخ - نسخه بهبود یافته
    """
    try:
        if not question or not previous_answer:
            return None
            
        # اگر پاسخ کوتاه است، کل آن را برگردان
        if len(previous_answer) < 100:
            return previous_answer
            
        stopwords = ["است", "هست", "آیا", "چیست", "چیه", "را", "از", "در", "به", "برای", "می", "که", "این", "آن"]
        words = [w.strip("؟!.") for w in question.split() if w not in stopwords and len(w) > 1]

        if not words:
            return None
            
        sentences = [s.strip() for s in previous_answer.split(".") if s.strip()]

        for key in words:
            for s in sentences:
                if key in s and len(s) > 10:  # فقط جملات معنی‌دار
                    return s.strip()

        # اگر پیدا نکردی، اولین جمله معنی‌دار را برگردان
        for s in sentences:
            if len(s) > 10:
                return s.strip()

        return None
        
    except Exception as e:
        print(f"⚠️ خطا در extract_related_part: {e}")
        return None

def save_to_file(question, answer, filename="Questions_database.txt"):
    if not answer:
        return
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{answer}")
def load_memory_lines(filename="Questions_database.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()  # خروجی لیست 

def similarity_fa(s1, s2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([s1, s2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


def run_search(subject):
    # جستجوی هوشمند
    search_results = get_links(subject, num=3)
    if search_results:
        combined_content = []
        for i, result in enumerate(search_results, 1):
            # استخراج محتوا از هر لینک
            content = extract_content(result["href"])        
            if content and not content.startswith("❌"):
                # خلاصه‌سازی محتوا
                summary = content[:500] + "..." if len(content) > 500 else content
                combined_content.append(f"📚 {result['title']}\n{summary}")
    
        if combined_content:
            final_response = "🔍 نتایج جستجو:\n\n" + "\n\n".join(combined_content[:2])
            return final_response
        else:
            return "متأسفانه محتوای مناسبی از صفحات وب یافت نشد."
    else:
        return "متأسفانه در جستجوی اینترنتی اطلاعاتی یافت نشد."
    

def needs_internet_search_en_v4(text):
    """
    Smarter English-only check for internet search necessity.
    - Uses substring matching
    - Handles multi-word keywords more robustly
    - Considers question, keywords, and sentence length
    """
    text_lower = text.lower().strip()
    
    
    is_question = text_lower.endswith('?') or any(text_lower.startswith(w) for w in ['what','how','who','which','when','where','can you'])
    
    search_keywords = [
        'method','tutorial','new','news','statistics','research','study','definition','meaning',
        'usage','advantages','disadvantages','history','python','artificial intelligence',
        'machine learning','data analysis','programming','code','algorithm','functions','class','object',
        'can you','about'
    ]
    
    words = text_lower.split()
    
    keyword_hits = 0
    for kw in search_keywords:
        kw_tokens = kw.split()
        for i in range(len(words) - len(kw_tokens) + 1):
            if words[i:i+len(kw_tokens)] == kw_tokens:
                keyword_hits += 1
                break  

    
    score = 0
    if is_question:
        score += 1
    score += keyword_hits * 2
    if len(words) > 5:
        score += 1
    
    return score >= 3

def clean_message(message):
    return re.sub(r'[^a-zA-Z\s]', '', message).lower()

# بررسی چندکلمه‌ای (هر کلمه از عبارت در پیام باشد)
def phrase_in_message(phrase, message):
    words = phrase.split()
    return all(word in message for word in words)

request_verbs = [
    "help", "show", "give", "send", "tell", "explain",
    "provide", "teach", "find", "make", "walk", "assist",
    "guide", "support", "review", "clarify", "instruct",
    "demonstrate", "outline", "describe"
]

request_phrases = [
    "can you", "could you", "would you",
    "i need", "i want", "let me", "please", "could i", "would i"
]

request_indirect = [
    "it would be great if", "i would appreciate", "could someone",
    "would anyone", "i am looking for", "i am hoping", "i wonder if"
]

def is_request(message):
    message_clean = clean_message(message)
    score = 0
    
    # بررسی عبارات مستقیم
    for phrase in request_phrases:
        if phrase_in_message(phrase, message_clean):
            score += 2
    
    # بررسی افعال
    for verb in request_verbs:
        if verb in message_clean:
            score += 1
    
    # بررسی عبارات غیرمستقیم
    for indirect in request_indirect:
        if phrase_in_message(indirect, message_clean):
            score += 1.5
    
    return score > 2


def need_code(message):
    msg = message.lower()

    strong_patterns = [
        "write a program",
        "write code",
        "python code",
        "example code",
        "sample code",
        "show me code",
        "implement this",
        "how to code",
        "how do i implement",
        "how to implement",
        "write a function",
        "create a function"
    ]

    languages = ["python", "java", "c++", "c#", "javascript", "html", "css"]

    verbs = ["write", "generate", "create", "build", "implement", "simulate"]

    # عبارات خیلی واضح
    for p in strong_patterns:
        if p in msg:
            return True

    # اگر فعل + زبان بیاید
    for v in verbs:
        for lang in languages:
            if v in msg and lang in msg:
                return True

    # اگر کلمه program بیاید + فعل
    if "program" in msg:
        for v in verbs:
            if v in msg:
                return True

    return False