def get_quizz_prompt(retrieved_texte):
    prompt_QUIZ = '''
              Tu es un expert en quiz. A partir du texte ci-dessus qui represente des notes que j'ai prises pendant la lecture d'un livre
              tu dois creer un quiz composé de 3 questions les plus pertinentes qui permettent d'évaluer la 
              bonne compréhension du livre. Si tu reconnais de quel livre il s'agit, tu peux enrichir le quiz avec 
              des questions plus poussées, et tu peux même mentionner le livre si tu y arrives. \n
               Si tu vex faire reference au livre, tu dois dire selon le livre ou bien selon l'auteur. \n 
              Tu dois retourner un json comme ça : \n
              {
                  "action" : "quizz",
                  "quiz_qa" : [
                                {
                                  "q" : "question1",
                                  "a" : "response1"
                                },
                                {
                                  "q" : "question2",
                                  "r" : "response2"
                                },
                                {
                                  "q" : "question3",
                                  "r" : "response3"
                                }
                              ]
              }   
              ''' + f'\n\n Texte = {retrieved_texte}'
    return prompt_QUIZ

    
def get_corrector_prompt(q_a_user_reponses):
    prompt_CORRECTOR = '''
                  Tu es un expert en quiz et tu dois avoir corriger et attribuer une note entre 0 et 5 à un utilisateur qui repond 
                  à un quiz composé de 3 questions.\n
                  Tu reçois un json comportant les questions, les reponses attendues et les reponse de l'utilisateur.\n
                  Voici le json que tu reçois : \n ''' + f'\n\n Texte = {q_a_user_reponses}' + \
                  '''
                  q : correspond à la question posée. \n
                  r : correspond à la reponse attendue. \n
                  r_user : correspond à la reponse proposée par l'utilisateur.\n
                  \n
                  Tu dois retourner un json comme ça : \n
                  {
                    "action" : "evaluate_user_reponses"
                    "grades" : [
                                {
                                    "note" : "note de la question 1"
                                  },
                                  {
                                    "note" : "note de la question 2"
                                  },
                                  {
                                    "note" : "note de la question 3"
                                  }
                              ]
                  }
                  
                  \n
                  note : est la note que tu attribues à l'utilisateur. Tu évalues la reponse de l'utilisateur par rapport à la reponse attendue. Elle doit sous la forme d'un nombre.
                  '''
    return prompt_CORRECTOR


def get_prompt_TEACHER(subject) :
  prompt_TEACHER = '''Tu es un expert en culture générale, et tu adoptes le rôle d'un professeur dispensant un cours sur un sujet que l'on te demande.

Le sujet d'aujourd'hui porte sur : ''' + subject + '''.

Tu dois développer ce sujet de manière approfondie et fournir un cours bien structuré, complet et détaillé. Ta réponse doit être rendue sous la forme d'un JSON bien formaté, structuré comme suit :
{
   "head": {
      "titre": "Une reformulation captivante du titre du sujet",
      "illustration": "Ajoute un emoji pertinent pour illustrer le sujet, compatible avec Notion"
   },
   "body": {
      "Introduction": {
         "titre": "Introduction au sujet. Tu peux formuler comme tu le souhaite le titre de l'introduction",
         "texte": "Une introduction claire et engageante sur le sujet, avec un aperçu des points à aborder"
      },
      "Point_1": {
         "titre": "1- Titre du premier point",
         "texte": "Développement détaillé du premier point, avec des exemples ou explications précises"
      },
      "Point_2": {
         "titre": "2- Titre du deuxième point",
         "texte": "Développement détaillé du deuxième point, en l'étayant d'exemples et de faits"
      },
      "Point_3": {
         "titre": "3- Titre du troisième point",
         "texte": "Développement détaillé du troisième point, avec des références ou éléments pertinents"
      },
      "Point_4": {
         "titre": "4- Titre du quatrième point",
         "texte": "Développement détaillé du quatrième point, avec des explications et exemples supplémentaires"
      },
      "Point_5": {
         "titre": "5- Titre du cinquième point",
         "texte": "Développement détaillé du cinquième point, avec des informations finales sur le sujet"
      },
      "Conclusion": {
         "titre": "Conclusion",
         "texte": "Résumé de l'ensemble du sujet et réflexion finale, avec des ouvertures possibles"
      }
   }
}


'''
  return prompt_TEACHER