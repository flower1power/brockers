import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL_API: str = os.getenv("BASE_URL_API")
KAFKA_PRODUCER: str = os.getenv("KAFKA_PRODUCER")
