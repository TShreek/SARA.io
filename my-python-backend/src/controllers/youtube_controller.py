from flask import request, jsonify
from services.youtube_service import YouTubeService

class YouTubeController:
    def __init__(self):
        self.youtube_service = YouTubeService()

    def fetch_related_videos(self):
        query = request.args.get('query')
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        videos = self.youtube_service.get_related_videos(query)
        return jsonify(videos)