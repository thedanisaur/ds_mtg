import json
import os
import re
import yaml

def convert_mana_cost(mana_string):
    # Regular expression to find all mana symbols
    # Match hybrid and phyrexian mana first (e.g., 2/R, W/U, G/P), then single letters/numbers
    pattern = r'\d+\/[WUBRGCS]|\d+|[WUBRGCSXYZ]\/[WUBRGCS]|[WUBRGCSXYZ]'
    
    # Find all matching symbols
    symbols = re.findall(pattern, mana_string)
    
    # Wrap each symbol in {}
    wrapped = ''.join(f'{{{s}}}' for s in symbols)
    
    return wrapped

if __name__ == '__main__':

    # Settings

    settings = '''
[Settings]
{
    "layouts": {
        "Default": {
            "weight": 1,
            "slots": [
                {
                    "name": "RareOrMythic", 
                    "count": 1, 
                    "sheets": [
                        {"name": "Rare",   "weight": 8}, 
                        {"name": "Mythic", "weight": 1}
                    ]
                },
                {"name": "Uncommon", "count": 3 },
                {"name": "Common",   "count": 11},
            ]
        }
    }
}'''

    # Configurations
    folder_path = "./cards"
    order = [ 'colorless', 'white', 'blue', 'black', 'red', 'green', 'gold', 'artifact', 'land' ]
    cards_by_rarity = { 'Common': [], 'Uncommon': [], 'Rare': [], 'Mythic': [] }

    # Build list of cards
    image_markdown = '\n'
    for folder in order:
        path = f"{folder_path}/{folder}/"
        for file in sorted(os.listdir(path)):
            if file.lower().endswith('.yaml'):
                with open(f"{path}{file}", "r", encoding="utf-8") as card_file:
                    content = yaml.safe_load(card_file)
                    for card_name in content:
                        # The image name is just the card name minus "card_"
                        image_name = card_name.split('_', 1)[1]
                        card = content[card_name]['front']
                        cards_by_rarity[card['rarity']].append({
                            'name': card['name'],
                            'type': card['type'],
                            'mana_cost': convert_mana_cost(str(card['cost'])),
                            'image': f"https://raw.githubusercontent.com/thedanisaur/ds_mtg/refs/heads/master/cards/{folder}/{image_name}.jpeg"
                        })

    # Write back the updated content
    draftmancer_file = 'draftmancer.txt'
    with open('draftmancer.txt', "w", encoding="utf-8") as file:
        print(f"Writing custom cards")
        file.write('[CustomCards]\n')
        file.write('[\n')
        for rarity in cards_by_rarity:
            for index, cards in enumerate(cards_by_rarity[rarity]):
                file.write(f"{json.dumps(cards, indent=4)}")
                if index != len(cards_by_rarity[rarity]):
                    file.write(f",")
                file.write(f"\n")
        file.write(']\n')
        print(f"✅ Cards written")

        print(f"Writing settings")
        file.write(f"{settings}\n")
        print(f"✅ Settings written")

        print(f"Writing sheets")
        for rarity in cards_by_rarity:
            file.write(f"[{rarity}]\n")
            for card in cards_by_rarity[rarity]:
                # 3 packs per person
                # 8 people
                # 15 cards
                # 3 x 8 x 15 = 360 cards for a draft
                # Based on rarity breakdown c:11, u:3, r:1, m:1/8 we need to multiply the drafts
                # to 6 to see at least one of each mythic 3 x 8 x 1/8 = 3. 3 x 6 = 18
                # Following that logic we need c: 1584, u:432, r:144, m:18 total for proper distribution
                # 100 commons x 15 = 1500 (slightly under represented)
                # 62 uncommons x 7 = 434 (slightly over represented)
                # 45 rares x 3 = 135 (slightly under represented)
                # 18 mythics x 1 = 18 (exactly represented)
                if rarity == 'Common':
                    file.write('15 ')
                elif rarity == 'Uncommon':
                    file.write('7 ')
                elif rarity == 'Rare':
                    file.write('3 ')
                file.write(f"{card['name']}\n")
            file.write(f"\n")
        print(f"✅ Sheets written")
    print(f"✅ Updated '{draftmancer_file}'")
