# Utility script - not used by the app. Run manually to check current Groq models.

from groq import Groq
from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
models = client.models.list()

for m in models.data:
    print(m.id)