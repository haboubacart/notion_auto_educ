import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

             
def response_to_query(prompt, query='') -> json:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}, 
            ]
        )
    response = response.choices[0].message.content
    print(response)
    response = json.loads(response)
    
    """if response["action"] == "quizz" :
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
      return (grade)"""
        
    return response



