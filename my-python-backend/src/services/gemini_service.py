class GeminiService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.gemini.com/v1"

    def fetch_data(self, endpoint, params=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def process_data(self, data):
        # Implement data processing logic here
        return data