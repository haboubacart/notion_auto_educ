from src.usecases.generate_subject import usecase_generate_subject
from src.usecases.generate_quizz import usecase_generate_quizz
from config import  (NOTION_DATABASE_APPRENTISSAGE_ID,
                     NOTION_DATABASE_ID_SUJETS,
                     NOTION_DATABASE_SUJETS,
                     NOTION_DATABASE_QUIZZ_ID,
                     NOTION_FOMULAIRE_QUIZZ,
                     EMAIL,
                     EMAIL_PASSWORD,
                     CLIENT)


if __name__ == '__main__' :
    result = usecase_generate_subject(CLIENT, NOTION_DATABASE_SUJETS, NOTION_DATABASE_ID_SUJETS, NOTION_DATABASE_APPRENTISSAGE_ID, EMAIL, EMAIL_PASSWORD)
    if result == 0 :
        print('Pas de nouveau sujet à traiter')
    
    '''result = usecase_generate_quizz(CLIENT, NOTION_DATABASE_ID_SUJETS, NOTION_DATABASE_QUIZZ_ID)
    print(result)'''

    

