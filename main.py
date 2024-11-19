from src.chatgpt.prompts import get_prompt_TEACHER
from src.chatgpt.chatgpt import response_to_query
from src.notion.pages import (create_notion_page, 
                            extract_text_from_block,
                            last_subject_quizz_generation)

from config import  (NOTION_DATABASE_APPRENTISSAGE_ID,
                     NOTION_DATABASE_ID_SUJETS,
                     CLIENT)



if __name__ == '__main__' :
    """subject = "La data science"
    response = response_to_query(get_prompt_TEACHER(subject))
    subject_head = dict(response['value']['head'])
    subject_content = dict(response['value']['body'])
    create_notion_page(CLIENT, NOTION_DATABASE_APPRENTISSAGE_ID, subject_head, subject_content)
"""
    """last = get_id_livre_database(CLIENT, "e25dc3669ba142c49a999136ab49bd27")['results'][-1]
    print(json.dumps(last, indent=2))"""

    #print(last['properties']['id_page_notion_livre']['title'][0]['text']['content'])
    last_subject_quizz_generation(CLIENT, NOTION_DATABASE_ID_SUJETS)

