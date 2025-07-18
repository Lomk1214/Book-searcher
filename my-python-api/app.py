from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

@app.route('/search', methods=['POST'])
def search_books():
    data = request.get_json()
    query = data.get('book_name', '').strip()

    if not query:
        return jsonify({"error": "No book name provided"}), 400

    search_url = f"https://www.goodreads.com/search?q={query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    try:
        res = requests.get(search_url, headers=headers)
        res.raise_for_status()
    except Exception as e:
        return jsonify({"error": "Failed to fetch Goodreads search results"}), 500

    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.select('table.tableList tr')[:20]

    books = []

    for row in rows:
        title_tag = row.find('a', class_='bookTitle')
        img_tag = row.find('img')

        if title_tag and img_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.goodreads.com" + title_tag['href']
            image = img_tag['src']

            books.append({
                "title": title,
                "link": link,
                "image": image
            })

    return jsonify(books)

if __name__ == '__main__':
    app.run(port=3001, debug=True)


#     for row in rows:
#         title_elem = row.select_one("a.bookTitle span")
#         author_elem = row.select_one("a.authorName span")
#         link_elem = row.select_one("a.bookTitle")
#         image_elem = row.select_one("img")

#         if title_elem and author_elem and link_elem:
#             results.append({
#                 "title": title_elem.text.strip(),
#                 "author": author_elem.text.strip(),
#                 "link": "https://www.goodreads.com" + link_elem['href'],
#                 "image": image_elem['src'] if image_elem else None
#             })

#     return results

# @app.route('/search', methods=['POST'])
# def handle_search():
#     data = request.get_json()
#     search = data.get('query', '')
#     print(f"Received query: {search}")
    
#     result = search_goodreads(search)
#     return jsonify(result or [])

    
# if __name__ == '__main__':
#     app.run(port=3001)
