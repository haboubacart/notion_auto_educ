import re
import random
from datetime import datetime
import pytz

def convertir_markdown_en_rich_text(texte):
    """
    Convertit un texte en Markdown en rich_text compatible avec l'API Notion.
    """
    rich_text = []
    lines = texte.split("\n")
    for line in lines:
        # Vérifie si la ligne est une liste non ordonnée (- ou *)
        if re.match(r"^-*\s", line):
            content = line[2:].strip()  # Supprime le symbole de liste
            rich_text.append({
                "type": "text",
                "text": {"content": f"• {content}\n"},
                "annotations": {}
            })
        # Vérifie si la ligne est une liste ordonnée (1., 2., ...)
        elif re.match(r"^\d+\.\s", line):
            content = line.split(maxsplit=1)[1].strip()
            rich_text.append({
                "type": "text",
                "text": {"content": f"{content}\n"},
                "annotations": {}
            })
        else:
            # Recherche de gras (`**texte**`) et italique (`_texte_`)
            pattern_bold = r"\*\*(.*?)\*\*"
            pattern_italic = r"_(.*?)_"
            last_index = 0

            for match in re.finditer(f"{pattern_bold}|{pattern_italic}", line):
                start, end = match.span()
                # Ajouter le texte normal avant le style
                if start > last_index:
                    rich_text.append({
                        "type": "text",
                        "text": {"content": line[last_index:start]},
                        "annotations": {}
                    })

                # Ajouter le texte stylisé
                if match.group(1):  # Texte en gras
                    rich_text.append({
                        "type": "text",
                        "text": {"content": match.group(1)},
                        "annotations": {"bold": True}
                    })
                elif match.group(2):  # Texte en italique
                    rich_text.append({
                        "type": "text",
                        "text": {"content": match.group(2)},
                        "annotations": {"italic": True}
                    })

                last_index = end

            # Ajouter le reste du texte
            if last_index < len(line):
                rich_text.append({
                    "type": "text",
                    "text": {"content": line[last_index:]},
                    "annotations": {}
                })

            rich_text.append({"type": "text", "text": {"content": "\n"}})  # Ajoute une ligne vide

    return rich_text


def create_notion_page(client, database_id, subjet_head, subject_content):
    france_timezone = pytz.timezone('Europe/Paris')
    current_date = datetime.now(france_timezone).strftime("%Y-%m-%d %H:%M:%S")
    new_page = {
        "parent": {"database_id": database_id},
        "icon": {
            "type": "emoji",
            "emoji": subjet_head['illustration']
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": subjet_head['titre']
                        }
                    }
                ]
            },

            "Date": {  # Ajout de la propriété 'Date' avec la date courante
                "date": {
                    "start": current_date  # La clé 'start' contient la date de début
                }
            }
        },
        "children": []
    }
    new_page["children"].append(
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": subjet_head['illustration']
                        }
                    }
                ]
            }
        }
        
    )
    for _, content in subject_content.items() :
        new_page["children"].append({
            "object": "block",
            "type": "heading_2", 
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content['titre']
                        }
                    }
                ]
            }
        })
        new_page['children'].append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": convertir_markdown_en_rich_text(content['texte'])
                }
            }
        )
            
    try :
        response = client.pages.create(**new_page)
        page_created = {
                'page_created_id' : response['id'],
                'page_created_intitule' : response['properties']['Name']['title'][0]['text']['content'],
                'page_created_url' : response['url']
        }
        return page_created
    except :
        return 0

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

def update_id_livres_database(client, lecture_page_id, database_livre_id) :
     blocks = client.databases.query(database_id=lecture_page_id)
     for livre in blocks['results'] : 
        id = livre["id"]
        intitule = livre["properties"]["Name"]["title"][0]["text"]["content"]
        # Vérifier si la page existe déjà
        existing_pages = client.databases.query(
                **{
                "database_id": database_livre_id,
                "filter": {
                    "property": "id_page_notion_livre",
                    "title": {
                        "equals": id
                    }
                }
            }
        )
        # Si aucune page existante n'est trouvée, créer une nouvelle page
        if not existing_pages['results']:
            print("adding")
            client.pages.create(
                    **{
                        "parent": {
                            "database_id": database_livre_id
                        },
                        'properties': {
                            "id_page_notion_sujet" : {'title': [{'text': {'content': id}}]},
                            "intitule_sujet" : {'rich_text': [{'text': {'content': intitule}}]}
                        }
                    }
                )

def get_subject_to_treat(client, database_id) :
    subjects = client.databases.query(
        **{
        "database_id": database_id,
        "filter": {
            "property": "done",  
            "checkbox": {
                "equals": False  
            }
        }
    }
    )['results']
    if len(subjects) > 0 :
        subject_to_treat = random.choice(subjects)
        subject_line_id = subject_to_treat['id']
        subject_title = subject_to_treat['properties']['subject']['title'][0]['plain_text']
        return(subject_line_id, subject_title)
    return (0, 0)








  
  

    