"""Конфигурационный файл. Все переменные окружения
 задаются здесь и далее импортируем по файлам проекта"""
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
