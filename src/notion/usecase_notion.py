from pprint import pprint
import time

from text_block import (get_id_livre_database,
                        extract_text_from_block)
                                    
from quizz import (add_grade_to_quizz_row, 
                                 create_new_quizz_row,
                                 get_last_quizz_row_id,
                                 get_last_quizz)

from tache import (get_all_taches,
                   create_new_tache)

from src.chatgpt.prompts import (get_corrector_prompt,
                                 get_quizz_prompt)

from config import (NOTION_LECTURE_PAGE_ID,
                    NOTION_DATABASE_LIVRE_ID,
                    NOTION_DATABASE_QUIZZ_ID,
                    NOTION_DATABASE_TACHE_ID,
                    CLIENT)

from src.chatgpt.chatgpt import response_to_query

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
  retrieved_texte = f'Titre du livre : {livre['intitule_livre']} \n {extract_text_from_block(CLIENT, livre['id'])}'
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
  add_grade_to_quizz_row(CLIENT, 
                         NOTION_DATABASE_QUIZZ_ID, 
                         get_last_quizz_row_id(CLIENT, NOTION_DATABASE_QUIZZ_ID), 
                         grades, to_revise)
  return to_revise



if __name__=='__main__' : 
  
  quizz = cron_quizz_generation(CLIENT, NOTION_DATABASE_LIVRE_ID)
  print(quizz)

  """time.sleep(30)
  user_reponse = ["Quand tu es pauvre c'est pour toujours alors ne pas avoir d'argent est passager",
                      "la comptabilité et l'investissement",
                      "je ne sais pas"]"""
  #evaluate_user_quizz_response(CLIENT, NOTION_DATABASE_QUIZZ_ID, user_reponse)

  
  
  

    