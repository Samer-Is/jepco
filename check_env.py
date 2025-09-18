import os
from dotenv import load_dotenv

print("Before loading .env:")
print(f"OPENAI_API_KEY from os.getenv: {os.getenv('OPENAI_API_KEY')}")

load_dotenv()

print("After loading .env:")
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"OPENAI_API_KEY: {api_key[:20]}...{api_key[-20:]}")
else:
    print("No OPENAI_API_KEY found")

# Check if .env file exists and read it directly
try:
    with open('.env', 'r') as f:
        content = f.read()
        print("\n.env file content:")
        print(content)
except FileNotFoundError:
    print("No .env file found")
