from src.notion.quizz import (add_grade_to_quizz_row, 
                  create_new_quizz_row,
                  get_last_quizz_row_id,
                  get_last_quizz)

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

def generate_user_response_object(list_questions, list_responses, list_user_reponses):
  resp_object = []
  for question, response, user_response in zip(list_questions, list_responses, list_user_reponses):
    resp_object.append({
      "q" : question,
      "a" : response,
      "r_user" : user_response
    })
  return resp_object

def find_livre_to_quizz(client, NOTION_DATABASE_LIVRE_ID) : 
  result = {}
  livre_to_quizz = get_id_livre_database(client, NOTION_DATABASE_LIVRE_ID)[13]
  id = livre_to_quizz['id_page_notion_livre']
  intitule_livre = livre_to_quizz['intitule_livre']
  result['id'] = id
  result['intitule_livre'] = intitule_livre
  return result


def cron_quizz_generation(client, NOTION_DATABASE_LIVRE_ID) : 
  livre = find_livre_to_quizz(client, NOTION_DATABASE_LIVRE_ID)
  retrieved_texte = f'Titre du livre : {livre['intitule_livre']} \n {extract_text_from_block(client, livre['id'])}'
  print(retrieved_texte)
  quizz = response_to_query(get_quizz_prompt(retrieved_texte))
  print(quizz)
  create_new_quizz_row(client, 
                       NOTION_DATABASE_QUIZZ_ID, 
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
  
  

    