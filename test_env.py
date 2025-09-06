from dotenv import load_dotenv
import os

print("Before load_dotenv:")
print(f"LIVEKIT_API_KEY: {os.getenv('LIVEKIT_API_KEY')}")

load_dotenv()

print("\nAfter load_dotenv:")
print(f"LIVEKIT_API_KEY: {os.getenv('LIVEKIT_API_KEY')}")
print(f"LIVEKIT_API_SECRET: {os.getenv('LIVEKIT_API_SECRET')}")
print(f"LIVEKIT_URL: {os.getenv('LIVEKIT_URL')}")
