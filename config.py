from dotenv import load_dotenv
from notion_client import Client
import os
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_KEY")
NOTION_LECTURE_PAGE_ID = os.getenv("NOTION_LECTURE_PAGE_ID") 
NOTION_DATABASE_LIVRE_ID = os.getenv("NOTION_DATABASE_LIVRE_ID")
NOTION_DATABASE_QUIZZ_ID = os.getenv("NOTION_DATABASE_QUIZZ_ID")
NOTION_DATABASE_TACHE_ID = os.getenv("NOTION_DATABASE_TACHE_ID")
NOTION_DATABASE_APPRENTISSAGE_ID = os.getenv("NOTION_DATABASE_APPRENTISSAGE_ID")
NOTION_DATABASE_ID_SUJETS = os.getenv("NOTION_DATABASE_ID_SUJETS") 
NOTION_DATABASE_SUJETS = os.getenv("NOTION_DATABASE_SUJETS")
EMAIL = os.getenv("EMAIL") 
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") 
CLIENT = Client(auth=NOTION_TOKEN)
