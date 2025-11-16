from ddgs import DDGS
from newspaper import Article

def get_links(query, num=3):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num):
            results.append({
                "title": r['title'],
                "href": r['href']
            })
    return results
        
def extract_content(url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return (article.title + "\n\n" + article.text)[:2500]
        except Exception as e:
            return f"❌ خطا: {e}"