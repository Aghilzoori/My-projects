from ddgs import DDGS

def get_links(query, num=3):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num):
            results.append({
                "title": r['title'],
                "href": r['href']
            })
    return results