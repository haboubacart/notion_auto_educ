import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

             
def response_to_query(prompt, query='') -> json:
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
              {"role": "user", "content": prompt}
              ]
      )
  content = completion.choices[0].message.content
  print(content)
  try :
    response = json.loads(content)
  except KeyError as e:
      print(f"Clé manquante dans la réponse: {e}")
      response = None
  except json.JSONDecodeError as e:
      print(f"Erreur de décodage JSON: {e}")
      response = None
  
  if response["action"] == "quizz" :
    result = {}
    list_questions, list_responses = [],[]
    for q_a in response["quiz_qa"] :
        list_questions.append(q_a["q"])
        list_responses.append(q_a["a"])
    result['list_questions'] = list_questions
    result['list_responses'] = list_responses
    return (result)
  
  if response["action"] == "evaluate_user_reponses" :
    grade = 0
    for elm in response["grades"] : 
      grade+=elm["note"]
    return (grade)
      
  return response



