import os
import requests
from notion_client import Client
from rich import print
from typing import Dict, Any, Tuple
import re

# Initialize Notion client
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "17f84ade-96ac-81a1-a102-e594dd39f1fb"  # Replace with your database ID
client = Client(auth=NOTION_TOKEN)

def format_pokemon_name_for_url(name: str) -> str:
    """Format Pokemon name for Bulbapedia URL"""
    # Special case mappings
    special_names = {
        "nidoran-f": "Nidoran♀",
        "nidoran-m": "Nidoran♂",
        "mr-mime": "Mr._Mime",
        "ho-oh": "Ho-Oh",
        "mime-jr": "Mime_Jr.",
        "porygon-z": "Porygon-Z",
        "type-null": "Type:_Null",
        "jangmo-o": "Jangmo-o",
        "hakamo-o": "Hakamo-o",
        "kommo-o": "Kommo-o",
        "tapu-koko": "Tapu_Koko",
        "tapu-lele": "Tapu_Lele",
        "tapu-bulu": "Tapu_Bulu",
        "tapu-fini": "Tapu_Fini",
    }
    
    # Check if it's a special case
    if name.lower() in special_names:
        return special_names[name.lower()]
    
    # Replace hyphens with spaces and title case the name
    formatted_name = name.replace('-', ' ').title()
    # Replace spaces with underscores for URL
    formatted_name = formatted_name.replace(' ', '_')
    
    return formatted_name

def convert_to_roman(generation_num: int) -> str:
    """Convert generation number to roman numeral"""
    roman_numerals = {
        1: "I", 2: "II", 3: "III", 4: "IV",
        5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX"
    }
    return roman_numerals.get(generation_num, str(generation_num))

def get_best_sprite_url(sprites_data: Dict) -> Tuple[str, str]:
    """Get both the regular sprite and the largest artwork available"""
    # For regular sprite display in properties
    sprite_priorities = [
        'front_default',
        'front_shiny',
        'other.official-artwork.front_default',
        'other.home.front_default',
    ]
    
    # For cover image (prioritizing larger artwork)
    cover_priorities = [
        'other.official-artwork.front_default',
        'other.home.front_default',
        'front_default',
        'front_shiny',
    ]
    
    regular_sprite = None
    cover_sprite = None
    
    # Get regular sprite
    for priority in sprite_priorities:
        value = sprites_data
        for key in priority.split('.'):
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = None
                break
        if value:
            regular_sprite = value
            break
    
    # Get cover sprite (largest available)
    for priority in cover_priorities:
        value = sprites_data
        for key in priority.split('.'):
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = None
                break
        if value:
            cover_sprite = value
            break
    
    # Default placeholder if no sprites found
    placeholder = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/question-mark.png"
    return (regular_sprite or placeholder, cover_sprite or placeholder)

def fetch_pokemon_data(pokemon_id: int) -> Dict[str, Any]:
    """Fetch Pokemon data from PokeAPI including species data"""
    # Fetch basic Pokemon data
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    pokemon_response = requests.get(pokemon_url)
    
    # Fetch species data
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    species_response = requests.get(species_url)
    
    if pokemon_response.status_code == 200 and species_response.status_code == 200:
        data = pokemon_response.json()
        species_data = species_response.json()
        
        # Get both regular sprite and cover sprite
        sprite_url, cover_url = get_best_sprite_url(data['sprites'])
        
        # Get generation number and convert to roman
        generation_num = int(species_data['generation']['url'].split('/')[-2].split('-')[-1])
        generation_roman = convert_to_roman(generation_num)
        
        # Get types
        types = [t['type']['name'] for t in data['types']]
        
        # Get stats
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        
        # Get English flavor text and clean it
        flavor_texts = [
            entry['flavor_text'] 
            for entry in species_data['flavor_text_entries']
            if entry['language']['name'] == 'en'
        ]
        
        if flavor_texts:
            # Take the most recent flavor text and clean it
            flavor_text = flavor_texts[-1]
            # Clean up the text by removing extra spaces and special characters
            flavor_text = re.sub(r'[\n\f\r]+', ' ', flavor_text)
            flavor_text = re.sub(r'\s+', ' ', flavor_text).strip()
        else:
            flavor_text = "No description available."
        
        # Format name for URL
        pokemon_name = format_pokemon_name_for_url(data['name'])
        wiki_url = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name}_(Pok%C3%A9mon)"
        
        return {
            "name": data['name'].title().replace('-', ' '),  # Clean display name
            "number": data['id'],
            "height": data['height'] * 10,  # Convert to cm
            "weight": data['weight'] / 10,  # Convert to kg
            "types": types,
            "sprite_url": sprite_url,
            "cover_url": cover_url,
            "hp": stats['hp'],
            "attack": stats['attack'],
            "defense": stats['defense'],
            "special_attack": stats['special-attack'],
            "special_defense": stats['special-defense'],
            "speed": stats['speed'],
            "generation": generation_roman,
            "flavor_text": flavor_text,
            "wiki_url": wiki_url
        }
    return None

def create_notion_properties(pokemon_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create Notion properties from Pokemon data"""
    return {
        "Name": {
            "title": [{"text": {"content": pokemon_data["name"]}}]
        },
        "No": {
            "number": pokemon_data["number"]
        },
        "Height": {
            "number": pokemon_data["height"]
        },
        "Weight": {
            "number": pokemon_data["weight"]
        },
        "Type": {
            "multi_select": [{"name": t.lower()} for t in pokemon_data["types"]]
        },
        "HP": {
            "number": pokemon_data["hp"]
        },
        "Attack": {
            "number": pokemon_data["attack"]
        },
        "Defense": {
            "number": pokemon_data["defense"]
        },
        "Sp. Attack": {
            "number": pokemon_data["special_attack"]
        },
        "Sp. Defense": {
            "number": pokemon_data["special_defense"]
        },
        "Speed": {
            "number": pokemon_data["speed"]
        },
        "Generation": {
            "select": {"name": pokemon_data["generation"]}
        },
        "Category": {
            "rich_text": [{"text": {"content": "Pokémon"}}]
        },
        "Sprite": {
            "files": [{
                "name": f"{pokemon_data['name']}_sprite.png",
                "type": "external",
                "external": {
                    "url": pokemon_data["sprite_url"]
                }
            }]
        }
    }

def create_notion_page_content(pokemon_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create the content for the Notion page"""
    return {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": pokemon_data["flavor_text"]
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Learn more about this Pokémon on ",
                            }
                        },
                        {
                            "type": "text",
                            "text": {
                                "content": "Bulbapedia",
                                "link": {
                                    "url": pokemon_data["wiki_url"]
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }

def main():
    # Update first 10 Pokemon
    ids_missed = []
    for pokemon_id in range(1, 905):
        try:
            print(f"Fetching Pokemon #{pokemon_id}...")
            pokemon_data = fetch_pokemon_data(pokemon_id)
            
            if pokemon_data:
                properties = create_notion_properties(pokemon_data)
                page_content = create_notion_page_content(pokemon_data)
                
                # Create page in Notion with properties, content, and cover
                response = client.pages.create(
                    parent={"database_id": DATABASE_ID},
                    properties=properties,
                    **page_content,
                    icon=None,  # Optional: Add an icon if needed
                    cover={
                        "type": "external",
                        "external": {
                            "url": pokemon_data["cover_url"]
                        }
                    }
                )
                print(f"Successfully added {pokemon_data['name']} to Notion!")
            
        except Exception as e:
            ids_missed.append(pokemon_id)
            print(f"Error processing Pokemon #{pokemon_id}: {str(e)}")

    print(f"Pokemon IDs that Errored out: {ids_missed}")

if __name__ == "__main__":
    main() 