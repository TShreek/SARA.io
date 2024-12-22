#make sure you've done 
# pip install flask 
# pip install google-api-python-client

import requests
import openai
# do pip install openai requests

# === CONFIGURATION ===
import requests
import openai
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

# === CONFIGURATION ===
import requests
import openai
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

# === CONFIGURATION ===
OPENAI_API_KEY = "sk-proj-Tr4v5n-.......-rdx0v5-...."  # Replace with your OpenAI API key
GOOGLE_API_KEY = "AIzaSyA....."  # Replace with your Google Custom Search API key
GOOGLE_CSE_ID = "R42l-32....gAt4"  # Replace with your Custom Search Engine ID
YOUTUBE_API_KEY = "AIzaSyA....."  # Replace with your YouTube API key

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize Flask app
app = Flask(__name__)

def simplify_content(raw_text):
    """
    Simplify a given text using OpenAI's GPT API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"Explain this concept in simple terms: {raw_text}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error simplifying content: {e}"

def search_articles(query):
    """
    Search for articles using the Google Custom Search API.
    """
    try:
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "q": query,
        }
        response = requests.get(url, params=params)
        data = response.json()

        # Extract article titles and links
        results = []
        for item in data.get("items", []):
            title = item.get("title")
            link = item.get("link")
            results.append({"title": title, "link": link})

        return results
    except Exception as e:
        return f"Error fetching articles: {e}"

def search_youtube_videos(query):
    """
    Search for YouTube videos using the YouTube Data API.
    """
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(q=query, part="snippet", maxResults=5)
        response = request.execute()

        # Extract video titles and links
        results = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            link = f"https://www.youtube.com/watch?v={video_id}"
            results.append({"title": title, "link": link})

        return results
    except Exception as e:
        return f"Error fetching YouTube videos: {e}"

@app.route('/simplify', methods=['POST'])
def simplify():
    """
    API endpoint that receives a topic, fetches related articles, YouTube videos, 
    and returns simplified explanation, article links, and video links.
    """
    try:
        # Get topic from POST request
        topic = request.json.get('topic')

        # Step 1: Fetch raw articles using Google Custom Search
        articles = search_articles(topic)

        # Step 2: Fetch related YouTube videos
        youtube_videos = search_youtube_videos(topic)

        # Step 3: Combine article snippets (or use Wikipedia for explanation)
        if isinstance(articles, list) and len(articles) > 0:
            raw_text = " ".join([article["title"] for article in articles])
        else:
            raw_text = "Unable to fetch related articles."

        # Step 4: Simplify the content using OpenAI's GPT
        simplified_text = simplify_content(raw_text)

        # Return the simplified text, article links, and YouTube video links as JSON
        return jsonify({
            "simplified_text": simplified_text,
            "articles": articles[:5],  # Limit to top 5 articles
            "youtube_videos": youtube_videos[:5]  # Limit to top 5 YouTube videos
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

