def create_notion_page(client, database_id, subjet_head, subject_content):
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
            

    response = client.pages.create(**new_page)
    if not response:
        print("Failed to create page.")


def write_text_to_block(client, block_id, text, type):
  client.blocks.children.append(
        block_id=block_id,
        children=[
            {
                "object": "block",
                "type": type,
                type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    )
  
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