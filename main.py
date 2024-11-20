from src.usecases.genarate_subject import usecase_generate_subject
from config import  (NOTION_DATABASE_APPRENTISSAGE_ID,
                     NOTION_DATABASE_ID_SUJETS,
                     NOTION_DATABASE_SUJETS,
                     EMAIL,
                     EMAIL_PASSWORD,
                     CLIENT)



if __name__ == '__main__' :
    result = usecase_generate_subject(CLIENT, NOTION_DATABASE_SUJETS, NOTION_DATABASE_ID_SUJETS, NOTION_DATABASE_APPRENTISSAGE_ID, EMAIL, EMAIL_PASSWORD)
    if result == 0 :
        print('Pas de nouveau sujet à traiter')


