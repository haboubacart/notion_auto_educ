from src.notion.quizz import (add_grade_to_quizz_row, 
                  create_new_quizz_row,
                  get_last_quizz_row_id,
                  get_last_quizz,
                  )

from src.chatgpt.prompts import (get_corrector_prompt,
                                 get_quizz_prompt)

from config import (NOTION_DATABASE_LIVRE_ID,
                    NOTION_DATABASE_QUIZZ_ID,
                    CLIENT)

from src.chatgpt.chatgpt import response_to_query


def create_notion_page(client, database_id, subjet_head, subject_content):
    new_page = {
        "parent": {"database_id": database_id},
        "icon": {
            "type": "emoji",
            "emoji": subjet_head['illustration']
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": subjet_head['titre']
                        }
                    }
                ]
            }
        },
        "children": []
    }
    new_page["children"].append(
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": subjet_head['illustration']
                        }
                    }
                ]
            }
        }
        
    )
    for _, content in subject_content.items() :
        new_page["children"].append({
            "object": "block",
            "type": "heading_1", 
            "heading_1": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content['titre']
                        }
                    }
                ]
            }
        })
        new_page['children'].append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [  
                        {
                            "type": "text",
                            "text": {
                                "content": content['texte']
                            }
                        }
                    ]
                }
            }
        )
            

    response = client.pages.create(**new_page)
    if not response:
        print("Failed to create page.")

  
def extract_text_from_block(client, block_id) :
    blocks = client.blocks.children.list(block_id=block_id)['results']
    extracted_text = ""
    for block in blocks :
        for _, value in block.items() :
            if isinstance(value, dict) and 'rich_text' in value :
                for text_item in value['rich_text'] :
                    if 'text' in text_item :
                        extracted_text += text_item['text']['content']
                extracted_text += "\n"
    return extracted_text

def update_id_livres_database(client, lecture_page_id, database_livre_id) :
     blocks = client.databases.query(database_id=lecture_page_id)
     for livre in blocks['results'] : 
        id = livre["id"]
        intitule = livre["properties"]["Name"]["title"][0]["text"]["content"]
        # Vérifier si la page existe déjà
        existing_pages = client.databases.query(
                **{
                "database_id": database_livre_id,
                "filter": {
                    "property": "id_page_notion_livre",
                    "title": {
                        "equals": id
                    }
                }
            }
        )
        # Si aucune page existante n'est trouvée, créer une nouvelle page
        if not existing_pages['results']:
            print("adding")
            client.pages.create(
                    **{
                        "parent": {
                            "database_id": database_livre_id
                        },
                        'properties': {
                            "id_page_notion_sujet" : {'title': [{'text': {'content': id}}]},
                            "intitule_sujet" : {'rich_text': [{'text': {'content': intitule}}]}
                        }
                    }
                )




def generate_user_response_object(list_questions, list_responses, list_user_reponses):
  resp_object = []
  for question, response, user_response in zip(list_questions, list_responses, list_user_reponses):
    resp_object.append({
      "q" : question,
      "a" : response,
      "r_user" : user_response
    })
  return resp_object


def last_subject_quizz_generation(client, database_id, quizz_database_id) : 
  res_last_item = client.databases.query(database_id=database_id)['results'][-1]
  last_subject = {
                "id_page_notion_sujet" : res_last_item["properties"]["id_page_notion_sujet"]["title"][0]["text"]["content"],
                "intitule_sujet" : res_last_item["properties"]["intitule_sujet"]["rich_text"][0]["text"]["content"]
                 }
  retrieved_texte = f'Titre du livre : {last_subject['intitule_sujet']} \n {extract_text_from_block(client, last_subject['id_page_notion_sujet'])}'
  print(retrieved_texte)
  quizz = response_to_query(get_quizz_prompt(retrieved_texte))
  create_new_quizz_row(client, 
                       quizz_database_id, 
                       str(quizz['list_questions']), 
                       str(quizz['list_responses']))

def evaluate_user_quizz_response(client, NOTION_DATABASE_QUIZZ_ID, user_reponse):
  last_quizz = get_last_quizz(client, NOTION_DATABASE_QUIZZ_ID)
  responses_to_quizz = generate_user_response_object(last_quizz['list_questions'], last_quizz['list_responses'], user_reponse)
  grades = response_to_query(get_corrector_prompt(responses_to_quizz))
  to_revise = grades<9
  add_grade_to_quizz_row(client, 
                         NOTION_DATABASE_QUIZZ_ID, 
                         get_last_quizz_row_id(client, NOTION_DATABASE_QUIZZ_ID), 
                         grades, to_revise)
  return to_revise
  
  

    