from transform import read_source_dataframe ,transform_data
import requests

from mistralai.client import MistralClient
import os

#https://console.mistral.ai/
#https://docs.mistral.ai/api/#tag/models/operation/retrieve_model_v1_models__model_id__get

api_key = os.environ["MISTRAL_API_KEY"]
endpoint = "https://api.mistral.ai/v1/models"
model_name = "mistralai/Mistral-7B"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(endpoint, headers=headers)

if response.status_code == 200:
    models = response.json()
    print(models)
else:
    print(f"Failed to retrieve models: {response.status_code}") 


