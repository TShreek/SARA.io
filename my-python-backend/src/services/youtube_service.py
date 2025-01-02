class YouTubeService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def fetch_related_videos(self, video_id):
        url = f"{self.base_url}/search?relatedToVideoId={video_id}&type=video&key={self.api_key}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None

    def get_video_details(self, video_id):
        url = f"{self.base_url}/videos?id={video_id}&key={self.api_key}&part=snippet,contentDetails"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None