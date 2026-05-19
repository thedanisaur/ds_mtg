import importlib
import json
import os
import re
import yaml

from generate_docs import CARD_ORDER
from generate_docs import CARD_PATH
from generate_docs import colors_from_mana_cost
from generate_docs import TYPE_BASIC
from generate_docs import TYPE_LAND

# 3 packs per person
# 8 people
# 16 cards
# 3 x 8 x 16 = 384 cards for a draft
# Based on rarity breakdown c:11, u:3, r:1, m:1/8 we need to multiply the drafts
# by 6 to see at least one of each mythic 3 x 8 x 1/8 = 3. 3 x 6 = 18
# Following that logic we need c: 1584, u:432, r:144, m:18 total for proper distribution
# c = 3 * 8 * 6 * 11 = 1584
# u = 3 * 8 * 6 * 3 = 432
# r = 3 * 8 * 6 * 1 = 144
# m = 3 * 8 * 6 * 1/8 = 18
# 102 commons x 16 = 1620 (slightly over represented)
# 80 uncommons x 6 = 480 (slightly over represented)
# 55 rares x 3 = 165 (slightly over represented)
# 18 mythics x 1 = 18 (exactly represented)
card_counts_dks = {
    'Common': '16 ',
    'Uncommon': '6 ',
    'LandUncommon': '6 ',
    'Rare': '3 ',
    'LandRare': '3 ',
    'Mythic': '1 ',
    'LandMythic': '1 ',
    'Basic': '8 ',
}

# 3 packs per person
# 8 people
# 16 cards
# 3 x 8 x 16 = 384 cards for a draft
# Based on rarity breakdown c:11, u:3, r:1, m:1/8 we need to multiply the drafts
# by 6 to see at least one of each mythic 3 x 8 x 1/8 = 3. 3 x 6 = 18
# Following that logic we need c: 1584, u:432, r:144, m:18 total for proper distribution
# c = 3 * 8 * 6 * 11 = 1584
# u = 3 * 8 * 6 * 3 = 432
# r = 3 * 8 * 6 * 1 = 144
# m = 3 * 8 * 6 * 1/8 = 18
# 102 commons x 16 = 1620 (slightly over represented)
# 80 uncommons x 6 = 480 (slightly over represented)
# 55 rares x 3 = 165 (slightly over represented)
# 18 mythics x 1 = 18 (exactly represented)
card_counts_lck = {
    'Common': '16 ',
    'Uncommon': '7 ',
    'LandUncommon': '28 ',
    'Rare': '7 ',
    'LandRare': '7 ',
    'Mythic': '1 ',
    'Basic': '8 ',
}

set_weights_all = {
    'dks': card_counts_dks,
    'lck': card_counts_lck,
}

def convert_mana_cost(mana_string):
    # Regular expression to find all mana symbols
    # Match hybrid and phyrexian mana first (e.g., 2/R, W/U, G/P), then single letters/numbers
    pattern = r'\d+\/[WUBRGCS]|\d+|[WUBRGCSXYZ]\/[WUBRGCS]|[WUBRGCSXYZ]'
    
    # Find all matching symbols
    symbols = re.findall(pattern, mana_string)
    
    # Wrap each symbol in {}
    wrapped = ''.join(f'{{{s}}}' for s in symbols)
    
    return wrapped

def get_colors(card):
    colors = []
    if card['type'] == TYPE_LAND:
        colors = colors_from_mana_cost(card.get('colors', []))
    elif len(colors_from_mana_cost(card['cost'])) != 0:
        colors = colors_from_mana_cost(card['cost'])
    else:
        colors = colors_from_mana_cost(card.get('color_indicator', ''))
    return colors

def _generate_card_list(set, cards_by_rarity):
    for card_type in CARD_ORDER:
        if card_type == 'token':
            continue
        path = f"{CARD_PATH}/{set}/{card_type}/"
        for file in sorted(os.listdir(path)):
            if file.lower().endswith('.yaml'):
                with open(f"{path}{file}", "r", encoding="utf-8") as card_file:
                    content = yaml.safe_load(card_file)
                    for card_name in content:
                        # The image name is just the card name minus "card_"
                        image_name = card_name.split('_', 1)[1]
                        card_front = content[card_name]['front']
                        card_back = content[card_name].get('back', None)
                        card = {
                            'name': card_front['name'],
                            'super': card_front['super'],
                            'type': card_front['type'],
                            'mana_cost': str(card_front['cost']),
                            'colors': get_colors(card_front),
                            'rarity': card_front['rarity'].lower(),
                            'rating': card_front.get('rating', 0),
                            'oracle_text': card_front['rules_text'],
                        }
                        if card_back is not None:
                            image_name_front = image_name + "_front"
                            image_name_back = image_name + "_back"
                            card['image'] = f"https://raw.githubusercontent.com/thedanisaur/ds_mtg/refs/heads/master/cards/{set}/{card_type}/{image_name_front}.jpeg"
                            card['back'] = {
                                'name': card_back['name'],
                                'super': card_back['super'],
                                'type': card_back['type'],
                                'mana_cost': str(card_back['cost']),
                                'colors': get_colors(card_back),
                                'rarity': card_back['rarity'].lower(),
                                'oracle_text': card_back['rules_text'],
                                'image': f"https://raw.githubusercontent.com/thedanisaur/ds_mtg/refs/heads/master/cards/{set}/{card_type}/{image_name_back}.jpeg"
                            }
                        else:
                            card['image'] = f"https://raw.githubusercontent.com/thedanisaur/ds_mtg/refs/heads/master/cards/{set}/{card_type}/{image_name}.jpeg"
                        if card_front['type'] == 'Land' and card_front['super'] == 'Basic':
                            cards_by_rarity[card_front['super']].append(card)
                        elif card_front['type'] == 'Land':
                            cards_by_rarity[card_front['type'] + card_front['rarity']].append(card)
                        else:
                            cards_by_rarity[card_front['rarity']].append(card)

    return cards_by_rarity

def _write_standard_settings(set, cards_by_rarity):
    module_name = f"draftmancer_{set}_standard_settings"
    module = importlib.import_module(module_name)
    # Write back the updated content for a standard draft
    draftmancer_standard = f"draftmancer_{set}_standard.txt"
    set_weights = set_weights_all.get(set, {})
    with open(draftmancer_standard, "w", encoding="utf-8") as file:
        print(f"{draftmancer_standard}: Writing custom cards")
        file.write('[CustomCards]\n')
        file.write('[\n')
        for rarity in cards_by_rarity:
            for index, cards in enumerate(cards_by_rarity[rarity]):
                file.write(f"{json.dumps(cards, indent=4)}")
                if index != len(cards_by_rarity[rarity]):
                    file.write(f",")
                file.write(f"\n")
        file.write(']\n')
        print(f"{draftmancer_standard}: ✅ Cards written")

        print(f"{draftmancer_standard}: Writing settings")
        file.write(f"{module.settings}\n")
        print(f"{draftmancer_standard}: ✅ Settings written")

        print(f"{draftmancer_standard}: Writing sheets")
        for rarity in cards_by_rarity:
            file.write(f"[{rarity}]\n")
            for card in cards_by_rarity[rarity]:
                weight = set_weights.get(rarity, '')
                if len(weight) == 0:
                    exit(f"missing card weight for rarity: {rarity}")
                else:
                    file.write(weight)
                file.write(f"{card['name']}\n")
            file.write(f"\n")
        print(f"{draftmancer_standard}: ✅ Sheets written")
    print(f"{draftmancer_standard}: ✅ Updated successfully")

def _write_no_rarity_settings(set, cards_by_rarity):
    module_name = f"draftmancer_{set}_no_rarity_settings"
    module = importlib.import_module(module_name)
    # Write back the updated content for a no rarity draft
    draftmancer_no_rarity = f"draftmancer_{set}_no_rarity.txt"
    with open(draftmancer_no_rarity, "w", encoding="utf-8") as file:
        print(f"{draftmancer_no_rarity}: Writing custom cards")
        file.write('[CustomCards]\n')
        file.write('[\n')
        for rarity in cards_by_rarity:
            for index, cards in enumerate(cards_by_rarity[rarity]):
                file.write(f"{json.dumps(cards, indent=4)}")
                if index != len(cards_by_rarity[rarity]):
                    file.write(f",")
                file.write(f"\n")
        file.write(']\n')
        print(f"{draftmancer_no_rarity}: ✅ Cards written")

        print(f"{draftmancer_no_rarity}: Writing settings")
        file.write(f"{module.settings}\n")
        print(f"{draftmancer_no_rarity}: ✅ Settings written")

        print(f"{draftmancer_no_rarity}: Writing sheets")
        file.write(f"[Common]\n")
        for rarity in cards_by_rarity:
            for card in cards_by_rarity[rarity]:
                if card['type'] == TYPE_LAND and card['super'] == TYPE_BASIC:
                    continue
                elif card['type'] == TYPE_LAND:
                    file.write(f"16 {card['name']}\n")
                else:
                    file.write(f"4 {card['name']}\n")
        print(f"{draftmancer_no_rarity}: ✅ Sheets written")
    print(f"{draftmancer_no_rarity}: ✅ Updated successfully")

def generate_draftmancer():
    # Configurations
    cards_by_rarity = { 'Common': [], 'Uncommon': [], 'Rare': [], 'Mythic': [], 'LandUncommon': [], 'LandRare': [], 'LandMythic': [], 'Basic': [] }

    for set_folder in sorted(os.listdir(CARD_PATH)):
        # skip folders that aren't sets
        if set_folder.startswith("_"):
            continue
        # Build list of cards
        cards_by_rarity = _generate_card_list(set_folder, cards_by_rarity)
        _write_standard_settings(set_folder, cards_by_rarity)
        _write_no_rarity_settings(set_folder, cards_by_rarity)
        cards_by_rarity = { 'Common': [], 'Uncommon': [], 'Rare': [], 'Mythic': [], 'LandUncommon': [], 'LandRare': [], 'LandMythic': [], 'Basic': [] }

if __name__ == '__main__':
    generate_draftmancer()
