from src.chatgpt.prompts import get_prompt_TEACHER
from src.chatgpt.chatgpt import response_to_query
from config import  (NOTION_DATABASE_APPRENTISSAGE_ID,
                    CLIENT)


# Initialize the Notion client with your integration token
def create_notion_page(database_id, subjet_head, subject_content):
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
            "type": "heading_1", 
            "heading_1": {
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
                    "rich_text": [  
                        {
                            "type": "text",
                            "text": {
                                "content": content['texte']
                            }
                        }
                    ]
                }
            }
        )
            

    response = CLIENT.pages.create(**new_page)
    
    if not response:
        print("Failed to create page.")
        

if __name__ == '__main__' :
    subject = "Haboubacar Tidjani Boukari"
    response = response_to_query(get_prompt_TEACHER(subject))
    subject_head = dict(response['head'])
    subject_content = dict(response['body'])
    create_notion_page(NOTION_DATABASE_APPRENTISSAGE_ID, subject_head, subject_content)