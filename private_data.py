from dotenv import load_dotenv
import os

load_dotenv("tasks/.private/.env.private")

def get(key):
    return os.getenv(key)
