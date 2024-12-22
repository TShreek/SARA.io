class GeminiController:
    def __init__(self, gemini_service):
        self.gemini_service = gemini_service

    def fetch_data(self, request):
        # Logic to handle fetching data from the Gemini API
        data = self.gemini_service.get_data(request.args)
        return data

    def process_data(self, request):
        # Logic to handle processing data from the Gemini API
        processed_data = self.gemini_service.process_data(request.json)
        return processed_data