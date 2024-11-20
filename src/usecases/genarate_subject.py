from src.notion.pages  import get_subject_to_treat, create_notion_page
from src.chatgpt.prompts import get_prompt_TEACHER
from src.chatgpt.chatgpt import response_to_query

def usecase_generate_subject(client, database_sujets_id, database_id_pages, database_apprentissage_id): 
    subject_line_id, subject_title = get_subject_to_treat(client, database_sujets_id)
    if  (subject_line_id, subject_title) != (0,0) :
        response = response_to_query(get_prompt_TEACHER(subject_title))

        subject_head = dict(response['value']['head'])
        subject_content = dict(response['value']['body'])

        # Creer la page notion su sujet
        page_created = create_notion_page(client, database_apprentissage_id, subject_head, subject_content)
        if page_created != 0 :

            # Marquer le sujet comme done
            client.pages.update(
                **{
                    "page_id": subject_line_id,
                    "properties": {
                        "done": {
                            "checkbox": True  
                        }
                    }
                }
            )

            # Ajouter les infos de la page
            
            client.pages.create(
                **{
                    "parent": {
                        "database_id": database_id_pages
                    },
                    'properties': {
                        'id_page_notion_sujet': {'title': [{'text': {'content': page_created['page_created_id']}}]},
                        'intitule_sujet': {'rich_text': [{'text': {'content': page_created['page_created_intitule']}}]},
                        'url_page': {'url': page_created['page_created_url']}
                    }
                }
            )
        return 1
        # Envoyer tout ce qui est notification
    return 0
            