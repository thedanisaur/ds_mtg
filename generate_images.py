if __name__ == '__main__':
    import os

    # Configurations
    folder_path = "./cards"
    markdown_file = "README.md"
    section_header = "## Full Set"
    order = [ 'colorless', 'white', 'blue', 'black', 'red', 'green', 'gold', 'artifact', 'land', 'token', 'basic']

    # Supported image types
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp')

    # Get sorted list of image files
    count = 0
    row_open = False
    image_markdown = '\n<table>\n'
    for folder in order:
        for file in sorted(os.listdir(f"{folder_path}/{folder}/")):
            if file.lower().endswith(image_extensions):
                formatted_title = file.rsplit('.', 1)[0].replace('_', ' ').title()
                if count % 2 == 0:
                    if row_open:
                        image_markdown += "</tr>\n"
                    image_markdown += "<tr>\n"
                    row_open = True

                # Add image with title above
                image_markdown += f"""    <td align="center">
        <strong>{formatted_title}</strong><br/>
        <img src="{folder_path}/{folder}/{file}" alt="{formatted_title}" width="400"/>
    </td>\n"""

                count += 1

    # Close the last open row and the table
    if row_open:
        image_markdown += "</tr>\n"
    image_markdown += "</table>\n"

    # Read the existing Markdown file
    with open(markdown_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Find the position of the header
    header_index = content.find(section_header)
    if header_index == -1:
        raise ValueError(f"Header '{section_header}' not found in {markdown_file}")

    # Keep content up to the header and that line
    header_line_end = content.find("\n", header_index) + 1
    new_content = content[:header_line_end] + "\n" + image_markdown + "\n"

    # Write back the updated content
    with open(markdown_file, "w", encoding="utf-8") as file:
        file.write(new_content)

    print(f"✅ Updated '{markdown_file}' with image list from '{folder_path}' after '{section_header}'")
