import os

from generate_docs import CARD_ORDER
from generate_docs import CARD_PATH
from generate_docs import IMAGE_EXTENSIONS

def _generate_table(set_path):
    # Get sorted list of image files
    count = 0
    row_open = False
    image_markdown = '\n<table>\n'
    for card_type in CARD_ORDER:
        for file in sorted(os.listdir(f"{set_path}/{card_type}/")):
            if file.lower().endswith(IMAGE_EXTENSIONS):
                formatted_title = file.rsplit('.', 1)[0].replace('_', ' ').title()
                if count % 2 == 0:
                    if row_open:
                        image_markdown += "</tr>\n"
                    image_markdown += "<tr>\n"
                    row_open = True

                # Add image with title above
                image_markdown += f"""    <td align="center">
        <img src="{set_path}/{card_type}/{file}" alt="{formatted_title}" width="400"/><br/>
        <strong>{formatted_title}</strong>
    </td>\n"""

                count += 1

    # Close the last open row and the table
    if row_open:
        image_markdown += "</tr>\n"
    image_markdown += "</table>\n"

    return image_markdown

def generate_images():
    # Configurations
    set_list_header_text = "# Set List"

    for set_folder in sorted(os.listdir(CARD_PATH)):
        # skip folders that aren't sets
        if set_folder.startswith("_"):
            continue
        image_markdown = _generate_table(f"{CARD_PATH}/{set_folder}")
        markdown_file = f"{set_folder}.md"

        # Read the existing Markdown file
        with open(markdown_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Find the position of the header
        header_index = content.find(set_list_header_text)
        if header_index == -1:
            raise ValueError(f"Header '{set_list_header_text}' not found in {markdown_file}")

        # Keep content up to the header and that line
        header_line_end = content.find("\n", header_index) + 1
        new_content = content[:header_line_end] + "\n" + image_markdown + "\n"

        # Write back the updated content
        with open(markdown_file, "w", encoding="utf-8") as file:
            file.write(new_content)

        print(f"✅ Updated '{markdown_file}' with image list from '{CARD_PATH}' after '{set_list_header_text}'")

if __name__ == '__main__':
    generate_images()
