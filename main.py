from flask import Flask, jsonify, request
from flask_cors import CORS
import bbc
import json

app = Flask(__name__)
CORS(app)

def get_news(language):
    news = bbc.news.get_news(language)
    categories = news.news_categories()

    news_data = []
    for category in categories:
        # Get the news for the category
        section_news = news.news_category(category)
        news_data.append(section_news)

    news_response = json.dumps(news_data, indent=4) 
    return news_response

@app.route('/news', defaults={'language': 'english'}, methods=['GET'])
@app.route('/news/<language>', methods=['GET'])
def fetch_news(language):
    try:
        # Check the requested language and fetch news accordingly
        if language.lower() == 'english':
            news = get_news(bbc.Languages.English)
        elif language.lower() == 'hindi':
            news = get_news(bbc.Languages.Hindi)
        else:
            return jsonify({"error": "Language not supported"}), 400

        # Return the news as a JSON response
        return jsonify(json.loads(news)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
