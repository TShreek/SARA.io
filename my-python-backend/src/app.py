from flask import Flask
from controllers.gemini_controller import GeminiController
from controllers.youtube_controller import YouTubeController
from controllers.openai_controller import OpenAIController

app = Flask(__name__)

# Initialize controllers
gemini_controller = GeminiController()
youtube_controller = YouTubeController()
openai_controller = OpenAIController()

# Set up routes
@app.route('/gemini', methods=['POST'])
def handle_gemini():
    return gemini_controller.handle_request()

@app.route('/youtube', methods=['POST'])
def handle_youtube():
    return youtube_controller.handle_request()

@app.route('/openai', methods=['POST'])
def handle_openai():
    return openai_controller.handle_request()

if __name__ == '__main__':
    app.run(debug=True)