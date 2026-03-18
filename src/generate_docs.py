import re

CARD_ORDER = [ 'colorless', 'white', 'blue', 'black', 'red', 'green', 'gold', 'artifact', 'land', 'token', 'basic']
CARD_PATH = "./cards"
# Supported image types
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp')

TYPE_ARTIFACT='Artifact'
TYPE_BASIC='Basic'
TYPE_CREATURE='Creature'
TYPE_ENCHANTMENT='Enchantment'
TYPE_INSTANT='Instant'
TYPE_LAND='Land'
TYPE_PLANESWALKER='Planeswalker'
TYPE_SORCERY='Sorcery'
TYPE_TOKEN='Token'

def colors_from_mana_cost(mana_cost):
    """
    Extract colors from a mana cost string.
    
    Args:
        mana_cost (str): Mana cost like '{G}{U}{2}{G/U}{X}'
    
    Returns:
        Set[str]: A set of color names (e.g., {'Green', 'Blue'})
    """
    valid_colors = {
        'G',
        'W',
        'U',
        'B',
        'R',
    }
    mana_cost_str = str(mana_cost)
    symbols = re.findall(r'\{(.*?)\}', mana_cost_str.upper())
    colors = set()

    for symbol in symbols:
        # Handle hybrid or Phyrexian like G/U, G/P
        parts = re.split(r'[\/]', symbol)
        for part in parts:
            if part in valid_colors:
                colors.add(part)
    
    return list(colors)

if __name__ == '__main__':
    from generate_cockatrice import generate_cockatrice
    from generate_draftmancer import generate_draftmancer
    from generate_images import generate_images

    generate_cockatrice()
    generate_draftmancer()
    generate_images()
