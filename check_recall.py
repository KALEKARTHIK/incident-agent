import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()
client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.environ["HINDSIGHT_API_KEY"],
)
result = client.recall(bank_id="incident-agent",
                       query="Hundreds of failed SSH login attempts")
for m in result.results:
    print(m.text)
    print("---")