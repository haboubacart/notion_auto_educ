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
  prompt_TEACHER = '''
   Tu es un expert en culture générale et tu adoptes le rôle d un spécialiste expliquant un sujet en profondeur.
   Le sujet d'aujourd'hui porte sur : ''' + subject + '''.
   Tu dois développer ce sujet de manière approfondie et fournir un cours bien structuré, complet et détaillé. 
   Ta réponse doit être rendue obligatoirement sous la forme d'un texte structuré comme suit :
   {
      "action": "generate_topic",
      "value": 
      {
         "head": 
         {
            "titre": "Une reformulation captivante du titre du sujet",
            "illustration": "Emoji pertinent pour illustrer le sujet, compatible avec Notion"
         },
         "body": 
         {
            "Introduction": {
               "titre": "Introduction au sujet. Tu peux formuler comme tu le souhaites le titre de l'introduction",
               "texte": "Propose une introduction engageante qui présente le sujet. L'introduction doivent être bien développée pour bien présenter le sujet, avec un aperçu des aspects qui seront explorés."
            },
            "Point_1": {
               "titre": "1- Titre du premier point",
               "texte": "Explique en profondeur le premier point du sujet, avec des exemples, des explications détaillées et des références pertinentes."
            },
            "Point_2": {
               "titre": "2- Titre du deuxième point",
               "texte": "Développe le deuxième point, en apportant des faits, des études ou des exemples précis pour mieux comprendre ce concept."
            },
            "Point_3": {
               "titre": "3- Titre du troisième point",
               "texte": "Présente le troisième point avec des détails clairs, des statistiques ou des éléments de contexte qui apportent de la valeur au sujet."
            },
            "Point_4": {
               "titre": "4- Titre du quatrième point",
               "texte": "Explore le quatrième point avec des explications détaillées, des exemples pratiques ou des illustrations pertinentes."
            },
            "Point_5": {
               "titre": "5- Titre du cinquième point",
               "texte": "Fournis une conclusion détaillée sur le cinquième point, incluant des informations finales et des perspectives intéressantes."
            },
            "Conclusion": {
               "titre": "Conclusion",
               "texte": "Fais un résumé des idées clés du sujet et propose des réflexions ou des ouvertures supplémentaires."
            },
            "Sources": {
               "titre": "Sources",
               "texte": "les 3 principales sources que tu recommandes pour aller plus loin dans le sujet, sous forme de liens URL. Une reference par ligne"
            }
         }
      }
   }
   Instructions supplémentaires :
   0 - Obligatoire : la sortie doit être une chaine de caractère, pas de code
   1 - Développement complet : Chacun des 5 points point doit être très détaillé (en 300 mots au moins), en appuyant les concepts par des faits réel. Ajoute des statistiques, des études, des exemples concrets ou des références académiques.
   2 - Structuration claire : Utilise de la mise en forme textuelle : gras, italique, listes, des retours à la ligne et des sous-points pour clarifier et structurer les idées.
   3 - Rigueur académique : Assure-toi que chaque point soit rigoureusement développé et bien soutenu par des informations fiables.
   4 - Sources : Indique les sources d informations fiables sous forme de liens URL. Pas de liste avec []
   '''
  return prompt_TEACHER

