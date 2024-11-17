from src.chatgpt.prompts import get_prompt_TEACHER
from src.chatgpt.chatgpt import response_to_query
from src.notion.usecase_notion import (create_notion_page, extract_text_from_block)
from config import  (NOTION_DATABASE_APPRENTISSAGE_ID,
                    CLIENT)



if __name__ == '__main__' :
    subject = "La data science"
    response = response_to_query(get_prompt_TEACHER(subject))
    subject_head = dict(response['value']['head'])
    subject_content = dict(response['value']['body'])
    create_notion_page(CLIENT, NOTION_DATABASE_APPRENTISSAGE_ID, subject_head, subject_content)

