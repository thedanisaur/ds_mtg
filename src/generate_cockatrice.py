import os
import re
import yaml

from generate_docs import CARD_ORDER
from generate_docs import CARD_PATH
from generate_docs import colors_from_mana_cost
from generate_docs import TYPE_BASIC
from generate_docs import TYPE_CREATURE
from generate_docs import TYPE_INSTANT
from generate_docs import TYPE_LAND
from generate_docs import TYPE_PLANESWALKER
from generate_docs import TYPE_SORCERY
from generate_docs import TYPE_TOKEN


long_name = {
    "DKS": "Dark Souls",
    "LCK": "Dark Souls: Lost Crowns of the King"
}

def creates_this_token(set, token):
    color_map = {
        '{W}': 'white',
        '{U}': 'blue',
        '{B}': 'black',
        '{R}': 'red',
        '{G}': 'green',
        '{C}': 'colorless',
        '{U/R}': 'blue and red',
    }

    cards = []
    for folder in CARD_ORDER:
        path = f"{CARD_PATH}/{set}/{folder}/"
        for file in sorted(os.listdir(path)):
            if file.lower().endswith('.yaml'):
                with open(f"{path}{file}", "r", encoding="utf-8") as card_file:
                    content = yaml.safe_load(card_file)
                    for card_name in content:
                        card_front = content[card_name]['front']
                        card_front_rules_text = card_front['rules_text'].lower()
                        token_name = token['name'].lower()
                        token_rules_text = token['rules_text'].lower().strip()
                        # exceptions for treasure tokens
                        token_rules_text = '' if token_name == 'treasure' else re.sub(r'\s*\(.*?\)', '', token_rules_text)
                        token_sub_type = '' if token_name == 'treasure' else token['sub'].lower()
                        color = '' if token_name == 'treasure' else color_map.get(token.get('color_indicator', ''), '')
                        if color in card_front_rules_text and token_name in card_front_rules_text and token_rules_text in card_front_rules_text and token_sub_type in card_front_rules_text:
                            cards.append(card_front['name'])

                        card_back = content[card_name].get('back', None)
                        if card_back:
                            card_back_rules_text = card_back['rules_text'].lower()
                            if color in card_back_rules_text and token_name in card_back_rules_text and token_rules_text in card_back_rules_text and token_sub_type in card_back_rules_text:
                                cards.append(card_back['name'])
    return ', '.join(cards)

def type_to_tablerow(type):
    if TYPE_CREATURE in type:
        return 2
    if TYPE_LAND == type:
        return 0
    if TYPE_INSTANT == type or TYPE_SORCERY == type:
        return 3
    else:
        return 1

def mana_cost_to_cmc(mana_cost, x_value=0):
    """
    Convert mana cost string like '{2}{G}{G}' to its converted mana cost (CMC).
    
    Args:
        mana_cost (str): Mana cost string, e.g. '{2}{G}{G}', '{X}{G}', '{G/U}', etc.
        x_value (int): Value to use for 'X' if present. Defaults to 0.
    
    Returns:
        int: Converted mana cost (CMC).
    """
    colors = {
        'G',
        'W',
        'U',
        'B',
        'R',
    }

    mana_cost_str = str(mana_cost)
    # Find all symbols like {2}, {G}, {X}, etc.
    symbols = re.findall(r'\{(.*?)\}', mana_cost_str.upper())
    
    cmc = 0
    for symbol in symbols:
        if symbol.isdigit():
            cmc += int(symbol)
        else:
            # All other types (G, U, R, B, W, C, S, G/U, G/P, etc.) count as 1
            cmc += 1
    return cmc

def create_card(set, card_front, card_back, image_url):
    # Adjust card name for tokens because there are different tokens with the same name and cockatrice can't figure that out.
    card_name = card_front['name']
    # if (TYPE_LAND == card_front['type'] and TYPE_BASIC in card_front['super']) or TYPE_TOKEN in card_front['super']:
    #     card_name = f"{card_front['name']} - DKS"
    if TYPE_TOKEN in card_front['super']:
        card_name = f"{card_front['name']} Token"

    general_tags = f"""        <name>{card_name}</name>
        <text>{card_front['rules_text'].strip()}</text>
        <prop>PROPERTIES
        </prop>
        <set rarity="{card_front['rarity']}" num="{card_front['number']}" picurl="{image_url}">{set.upper()}</set>"""

    super_type = f"{card_front['super']} " if len(card_front['super']) > 0 else ''
    sub_type = f" - {card_front['sub']}" if len(card_front['sub']) > 0 else ''
    type = f"{super_type}{card_front['type']}{sub_type}"
    property_tags = f"""<layout>{ 'normal' if card_back is None else 'transform' }</layout>
            <side>front</side>
            <type>{type}</type>
            <maintype>{card_front['type']}</maintype>
            <manacost>{card_front['cost']}</manacost>
            <cmc>{mana_cost_to_cmc(card_front['cost'])}</cmc>"""
    color_str = "".join(colors_from_mana_cost(card_front['cost']))
    if len(color_str) == 0:
        color_str = "".join(colors_from_mana_cost(card_front.get('color_indicator')))
    if len(color_str) != 0:
        property_tags += f"\n            <colors>{color_str}</colors>"

    # Type specific properties
    if TYPE_CREATURE in card_front['type']:
        property_tags += f"""
            <pt>{card_front['power']}/{card_front['toughness']}</pt>"""

    if TYPE_PLANESWALKER in card_front['type']:
        property_tags += f"""
            <loyalty>{card_front['loyalty']}</loyalty>"""

    # Transform cards
    if card_back:
        general_tags += f"""
        <related>{card_back['name']}</related>"""

    # Type token tag
    if TYPE_TOKEN in card_front['super']:
        related_cards = creates_this_token(set, card_front)
        general_tags += f"""
        <reverse-related>{related_cards}</reverse-related>
        <token>1</token>"""
    
    general_tags += f"""
        <tablerow>{type_to_tablerow(card_front['type'])}</tablerow>"""

    # Comes into play tapped
    if 'enters the battlefield tapped' in card_front['rules_text']:
        general_tags += f"""
        <cipt>1</cipt>"""

    card = f"\n{general_tags.replace('PROPERTIES', property_tags)}\n"
    return card

def _generate_set(set):
    # Build list of cards
    cards = []
    for folder in CARD_ORDER:
        path = f"{CARD_PATH}/{set}/{folder}/"
        for file in sorted(os.listdir(path)):
            if file.lower().endswith('.yaml'):
                with open(f"{path}{file}", "r", encoding="utf-8") as card_file:
                    content = yaml.safe_load(card_file)
                    for card_name in content:
                        # The image name is just the card name minus "card_"
                        image_name = card_name.split('_', 1)[1]
                        card_front = content[card_name]['front']
                        card_back = content[card_name].get('back', None)
                        image_name_front = image_name + '_front' if card_back is not None else image_name
                        image_url = f"https://raw.githubusercontent.com/thedanisaur/ds_mtg/refs/heads/master/cards/{set}/{folder}/{image_name_front}.jpeg"
                        card_front_xml = create_card(set, card_front, card_back, image_url)
                        card_front_xml = f"""    <card>{card_front_xml}    </card>\n"""
                        cards.append(card_front_xml)

                        if card_back:
                            # Reversing this for transform cards.
                            image_name_back = image_name + "_back"
                            image_url = f"https://raw.githubusercontent.com/thedanisaur/ds_mtg/refs/heads/master/cards/{set}/{folder}/{image_name_back}.jpeg"
                            card_back_xml = create_card(set, card_back, card_front, image_url)
                            card_back_xml = f"""    <card>{card_back_xml}    </card>\n"""
                            cards.append(card_back_xml)
    return cards

def _write_cockatrice_set_file(set, cards):
    # Write the file
    cockatrice_set_file = f"cockatrice_{set}.xml"
    with open(cockatrice_set_file, "w", encoding="utf-8") as file:
        print(f"{cockatrice_set_file}: Writing set")
        xml_start = f"""<?xml version="1.0" encoding="UTF-8"?>
<cockatrice_carddatabase version="4">
    <sets>
        <set>
        <name>{set.upper()}</name>
        <longname>{long_name.get(set.upper())}</longname>
        </set>
    </sets>
    <cards>
"""
        file.write(xml_start)
        for card in cards:
            file.write(card)
        xml_end = f"""</cards>\n</cockatrice_carddatabase>"""
        file.write(xml_end)
        print(f"{cockatrice_set_file}: ✅ Set written")

def generate_cockatrice():
    for set_folder in sorted(os.listdir(CARD_PATH)):
        # skip folders that aren't sets
        if set_folder.startswith("_"):
            continue
        # Build list of cards
        cards = _generate_set(set_folder)
        _write_cockatrice_set_file(set_folder, cards)

if __name__ == '__main__':
    generate_cockatrice()
