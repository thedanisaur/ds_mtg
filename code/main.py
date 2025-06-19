def fix_json_keys():
    with open('cards/artifact/artifact_cards.json', 'r') as file:
        content = file.read()
        print(content)

if __name__ == '__main__':
    fix_json_keys()