from dotenv import load_dotenv
import os

load_dotenv()

print("Testing environment variables...\n")

print("COMPOSIO_API_KEY:", "Loaded" if os.getenv("COMPOSIO_API_KEY") else "Missing")
print("OPENROUTER_API_KEY:", "Loaded" if os.getenv("OPENROUTER_API_KEY") else "Missing")
print("GREEN_API_URL:", os.getenv("GREEN_API_URL"))
print("GREEN_API_ID_INSTANCE:", os.getenv("GREEN_API_ID_INSTANCE"))
print("GREEN_API_TOKEN_INSTANCE:", "Loaded" if os.getenv("GREEN_API_TOKEN_INSTANCE") else "Missing")