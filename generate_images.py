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
    image_markdown = '\n'
    for folder in order:
        for file in sorted(os.listdir(f"{folder_path}/{folder}/")):
            if file.lower().endswith(image_extensions):
                formatted_title = file.rsplit('.', 1)[0].replace('_', ' ').title()
                # Generate Markdown for images
                # image_markdown += f"![{formatted_title}]({folder_path}/{folder}/{file})\n"
                image_markdown += f'<img src="{folder_path}/{folder}/{file}" alt="{formatted_title}" width="400" />&nbsp;'

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
