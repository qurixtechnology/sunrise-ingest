import requests
import pprint
from configs.settings import config

response = requests.get(
    f"https://api.hubapi.com/crm/v3/objects/notes?hapikey={config.HUBSPOT_API_KEY}"
)
pprint.pprint(response.json())
