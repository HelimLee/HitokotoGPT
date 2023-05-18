import requests
import json

class OpenAIAPI:
    def __init__(self, conauth):
        # Define the auth header
        self.url = 'https://api.openai.com/v1/chat/completions'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {conauth}'
        }
        self.model = 'gpt-3.5-turbo'
    def contentInit(self, messages):
        data = {
            'model': self.model,
            'messages': messages
        }
        self.json_data = json.dumps(data)
    def genRequest(self):
        response = requests.post(self.url, headers=self.headers, data=self.json_data)
        response = response.json()
        return response

    