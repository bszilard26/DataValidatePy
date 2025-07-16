# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL      = os.getenv("BASE_URL")      # e.g. https://reqres.in/api
API_KEY       = os.getenv("API_KEY")       # e.g. reqres-free-v1
TIMEOUT       = float(os.getenv("TIMEOUT", "5"))  # default 5 seconds
