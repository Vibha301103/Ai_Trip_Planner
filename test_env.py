# from dotenv import load_dotenv
# import os

# load_dotenv()

# print(os.getenv("GROQ_API_KEY"))
import requests

key = "11ff0aa3f144555a562b96146c4a0b5a"  # paste your real key just for this test

resp = requests.get(
    "https://maps.googleapis.com/maps/api/place/textsearch/json",
    params={"query": "restaurants in Boston", "key": key}
)
print(resp.status_code)
print(resp.json())