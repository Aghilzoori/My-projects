from newspaper import Article

def extract_content(url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return (article.title + "\n\n" + article.text)[:2500]
        except Exception as e:
            return f"❌ خطا: {e}"