import ast
from src.notion.pages import extract_text_from_block


from src.chatgpt.prompts import (get_corrector_prompt,
                                 get_quizz_prompt)

from src.chatgpt.chatgpt import response_to_query


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


def create_new_quizz_row(client, database_quizz_id, intitule_sujet, questions, responses):
    try : 
        new_page = {
            "parent": {
                "database_id": database_quizz_id
            },
            'properties': {
                'Intitule_sujet': {'rich_text': [{'text': {'content': intitule_sujet}}]},
                'Questions': {'title': [{'text': {'content': questions}}]},
                'Reponses': {'rich_text': [{'text': {'content': responses}}]}
            }
        }
        client.pages.create(**new_page)
        return 1
    except :
        return 0


def last_subject_quizz_generation(client, database_id, database_quizz_id) : 
    res_last_item = client.databases.query(database_id=database_id)['results'][-1]
    last_subject = {
                    "id_page_notion_sujet" : res_last_item["properties"]["id_page_notion_sujet"]["title"][0]["text"]["content"],
                    "intitule_sujet" : res_last_item["properties"]["intitule_sujet"]["rich_text"][0]["text"]["content"]
                    }
    retrieved_texte = f'Titre du sujet : {last_subject['intitule_sujet']} \n {extract_text_from_block(client, last_subject['id_page_notion_sujet'])}'
    quizz = response_to_query(get_quizz_prompt(retrieved_texte))
    response = create_new_quizz_row(client, 
                                    database_quizz_id, 
                                    last_subject['intitule_sujet'],
                                    str(quizz['list_questions']), 
                                    str(quizz['list_responses']))
    return response


def get_last_quizz(client, database_id) : 
    result = {}
    last_quizz = client.databases.query(database_id=database_id)['results'][0]['properties']
    list_questions = last_quizz['Questions']['title'][0]['plain_text']
    list_responses = last_quizz['Reponses']['rich_text'][0]['plain_text']

    result['list_questions'] = ast.literal_eval(list_questions)
    result['list_responses'] = ast.literal_eval(list_responses)

    return result

def generate_user_response_object(list_questions, list_responses, list_user_reponses):
  resp_object = []
  for question, response, user_response in zip(list_questions, list_responses, list_user_reponses):
    resp_object.append({
      "q" : question,
      "a" : response,
      "r_user" : user_response
    })
  return resp_object

def get_last_quizz_row_id(client, database_id) :
    return client.databases.query(database_id=database_id)['results'][0]['properties']['Identifiant']['unique_id']['number']

def add_grade_to_quizz_row(client, database_id, row_id, note, a_reviser=False):
    page_id = get_last_quizz_row_id(client, database_id, row_id)
    if page_id:
        client.pages.update(
            page_id=page_id,
            properties={
                'Identifiant': {'rich_text': [{'text': {'content': f'QUIZZ{row_id}'}}]},
                'Note': {'number': note},
                'A_Reviser': {'checkbox': a_reviser}
            }
        )
    else:
        print(f"Page with Identifiant 'QUIZZ{row_id}' not found.")


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








