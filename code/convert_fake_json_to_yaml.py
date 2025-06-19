import re


def fix_json_keys(content):
    lines = content.splitlines()

    for index in range(len(lines) - 1, -1, -1):
        # Change strings to int where the values of the strings are numbers
        if ':' in lines[index]:
            key, value = lines[index].split(':', 1)
            key = key.replace('\"', '')
            value = value.strip()
            if len(value) > 2 and value[-1] == ',':
                value = value[:len(value) - 1]
            try:
                value = int(value.replace(',', '').replace('"', ''))
            except Exception as e:
                value = value
            lines[index] = f"{key}: {value}"

        # Make the rules text multiline again
        if '\\n' in lines[index]:
            key, value = lines[index].split(':', 1)
            value = f"|\n        {value[2:-1]}"
            value = value.replace('\\n', '\n        ')
            lines[index] = f"{key}: {value}"

        # Add the front key
        name_line = lines[index + 1] if index < len(lines) - 1 else lines[index]
        if 'card:' in lines[index] and 'name' in name_line:
            lines.insert(index + 1, "  front:")
            # now indent all lines from our position to the next card
            for i in range(index + 1, len(lines)):
                done = lines[i].strip().startswith("card")
                if done:
                    break
                else:
                    lines[i] = f"  {lines[i]}"

        # Fix the card name key value
        name_line = lines[index + 2] if index < len(lines) - 2 else lines[index]
        if 'card:' in lines[index]:
            name = name_line.split(':')[1].replace(' ', '_').replace('\'', '').replace('\"', '').replace(',', '').replace('\n', '').lower()
            lines[index] = f"  card{name}:"
        
        if 'front: {' in lines[index].strip():
            lines[index] = '    front:'
        if 'back: {' in lines[index].strip():
            lines[index] = '    back:'

        # Remove curly braces
        if '{' == lines[index].strip() or '}' == lines[index].strip() or '},' == lines[index].strip():
            del lines[index]

    return '\n'.join(lines)


def fix_rules_text(content):
    pattern = r'("rules_text"\s*:\s*")(.+?)(",)'

    def replace_newlines(match):
        start, rules_text, end = match.groups()
        lines = rules_text.split('\n')
        stripped_lines = [line.strip() for line in lines]
        joined = '\\n'.join(stripped_lines)
        return f'{start}{joined}{end}'

    return re.sub(pattern, replace_newlines, content, flags=re.DOTALL)


if __name__ == '__main__':
    color = 'white'
    old_filename = f"../cards/{color}/{color}_cards.json"
    new_filename = f"../cards/{color}/{color}_cards.yaml"
    with open(old_filename, 'r') as file:
        content = file.read()
    content = fix_rules_text(content)
    content = fix_json_keys(content)
    with open(new_filename, 'w') as f:
        f.write(content)
