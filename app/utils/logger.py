# logger.py

from loguru import logger
from app.config import LOG_PATH
import os

# logs klasörünü oluştur
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logger.add(LOG_PATH, rotation="1 MB", retention="10 days", level="INFO")
