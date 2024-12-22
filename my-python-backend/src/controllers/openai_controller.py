class OpenAIController:
    def __init__(self, openai_service):
        self.openai_service = openai_service

    async def generate_summary(self, req, res):
        user_input = req.json.get('input')
        summary = await self.openai_service.get_summary(user_input)
        res.json({'summary': summary})

    async def fetch_response(self, req, res):
        user_input = req.json.get('input')
        response = await self.openai_service.get_response(user_input)
        res.json({'response': response})