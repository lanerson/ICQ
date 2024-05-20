from dotenv import load_dotenv
import os

def get_token():
    load_dotenv()
    return os.getenv('API_TOKEN')