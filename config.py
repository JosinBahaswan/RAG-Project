import os
from dotenv import load_dotenv

load_dotenv() 

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
BASE_URL = "https://openrouter.ai/api/v1"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

CHAT_MODELS = [
    "nvidia/nemotron-3.5-lightning:free",
    "thinkingmachines/inkling-small:free",
    "nex-agi/nex-n2.5-pro:free",
]   # sebelumnya: "minimax/minimax-m3:free"          # model untuk generate jawaban
EMBED_MODEL = "openai/text-embedding-3-small"    # model untuk embedding