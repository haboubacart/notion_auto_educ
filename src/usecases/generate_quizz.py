from src.notion.quizz import last_subject_quizz_generation


def usecase_generate_quizz(client, database_id, quizz_database_id) :
    # Generer le quizz et l'ajouter dans la base 
    last_subject_quizz_generation(client, database_id, quizz_database_id)

    # Generer le formulaire et envoyer une notif
    
