
# dont forget to install dependencies, ask chatgpt for help if u want
from flask import Flask, request, jsonify
import requests
import openai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from pytesseract import image_to_string
from PIL import Image
import os

# Load environment variables from .env file
load_dotenv()

# Access API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

def simplify_content(raw_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Explain this concept in simple terms: {raw_text}"}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error simplifying content: {e}"

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_image(image_path):
    try:
        text = image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"Error extracting text from image: {e}"

def search_articles(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "q": query,
        }
        response = requests.get(url, params=params)
        data = response.json()

        results = []
        for item in data.get("items", []):
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet")
            results.append({"title": title, "link": link, "snippet": snippet})

        return results
    except Exception as e:
        return f"Error fetching articles: {e}"

def search_youtube_videos(query):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": YOUTUBE_API_KEY,
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 5
        }
        response = requests.get(url, params=params)
        data = response.json()

        results = []
        for item in data.get("items", []):
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            video_id = item["id"]["videoId"]
            link = f"https://www.youtube.com/watch?v={video_id}"
            results.append({"title": title, "description": description, "link": link})

        return results
    except Exception as e:
        return f"Error fetching YouTube videos: {e}"

def calculate_relevance(topic, text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"How relevant is this text to the topic '{topic}'? Rate it on a scale of 0 to 10: {text}"}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error calculating relevance: {e}"

# API endpoints

@app.route('/simplify', methods=['POST'])
def simplify():
    data = request.get_json()
    raw_text = data.get('text')
    if raw_text:
        simplified_text = simplify_content(raw_text)
        return jsonify({'simplified_text': simplified_text})
    return jsonify({'error': 'No text provided'}), 400

@app.route('/extract_text', methods=['POST'])
def extract_text():
    file = request.files.get('file')
    file_type = request.form.get('file_type')
    
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)
    
    if file_type == "pdf":
        text = extract_text_from_pdf(file_path)
    elif file_type == "image":
        text = extract_text_from_image(file_path)
    else:
        return jsonify({'error': 'Invalid file type'}), 400
    
    os.remove(file_path)  # Clean up the file after processing
    return jsonify({'extracted_text': text})

@app.route('/search_articles', methods=['POST'])
def search_for_articles():
    data = request.get_json()
    query = data.get('query')
    if query:
        articles = search_articles(query)
        return jsonify({'articles': articles})
    return jsonify({'error': 'No query provided'}), 400

@app.route('/search_youtube', methods=['POST'])
def search_for_videos():
    data = request.get_json()
    query = data.get('query')
    if query:
        videos = search_youtube_videos(query)
        return jsonify({'videos': videos})
    return jsonify({'error': 'No query provided'}), 400

@app.route('/calculate_relevance', methods=['POST'])
def calculate_video_relevance():
    data = request.get_json()
    topic = data.get('topic')
    text = data.get('text')
    if topic and text:
        relevance = calculate_relevance(topic, text)
        return jsonify({'relevance': relevance})
    return jsonify({'error': 'Topic or text not provided'}), 400

if __name__ == "__main__":
    app.run(debug=True)


