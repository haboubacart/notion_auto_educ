import ast

def get_last_quizz(client, database_id) : 
    result = {}
    last_quizz = client.databases.query(database_id=database_id)['results'][0]['properties']
    list_questions = last_quizz['Questions']['title'][0]['plain_text']
    list_responses = last_quizz['Reponses']['rich_text'][0]['plain_text']

    result['list_questions'] = ast.literal_eval(list_questions)
    result['list_responses'] = ast.literal_eval(list_responses)

    return result

def get_last_quizz_row_id(client, database_id) :
    return client.databases.query(database_id=database_id)['results'][0]['properties']['Identifiant']['unique_id']['number']

def create_new_quizz_row(client, database_id, questions, responses):
    client.pages.create(
        **{
            "parent": {
                "database_id": database_id
            },
            'properties': {
                'Questions': {'title': [{'text': {'content': questions}}]},
                'Reponses': {'rich_text': [{'text': {'content': responses}}]}
            }
        }
    )

def find_quizz_row_page_id(client, database_id, row_id):
    response = client.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "property": "Identifiant",
                "number": {
                    "equals": row_id
                }
            }
        }
    )
    results = response.get('results')
    if results:
        return results[0]['id']
    return None

def add_grade_to_quizz_row(client, database_id, row_id, note, a_reviser=False):
    page_id = find_quizz_row_page_id(client, database_id, row_id)
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

def find_subject_to_quizz(client, database_id) : 
  result = {}
  last_subject = client.databases.query(database_id=database_id)['results'][0]['properties']
  list_questions = last_subject['Questions']['title'][0]['plain_text']
  list_responses = last_quizz['Reponses']['rich_text'][0]['plain_text']
  livre_to_quizz = get_id_livre_database(client, database_id)[13]
  id = livre_to_quizz['id_page_sujet_livre']
  intitule_livre = livre_to_quizz['intitule_sujet']
  result['id'] = id
  result['intitule_livre'] = intitule_livre
  return result


def get_id_livre_database(client, database_id):
    bd_data_response =  client.databases.query(database_id=database_id)
    content = []
    for item in bd_data_response['results']:
       content.append(
          {
             "id_page_notion_livre" : item["properties"]["id_page_notion_livre"]["title"][0]["text"]["content"],
             "intitule_livre" : item["properties"]["intitule_livre"]["rich_text"][0]["text"]["content"]
          }
       )
    return(content)