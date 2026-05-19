import re
from pathlib import Path
from generate_docs import CARD_ORDER

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


# -----------------------------
# NORMALIZE NAME
# -----------------------------

def normalize_name(name: str) -> str:
    name = name.strip().lower()
    name = name.replace("'", "")
    name = name.replace("-", "_").replace(" ", "_")
    name = name.replace(",", "")
    return re.sub(r"_+", "_", name).strip("_")


# -----------------------------
# SPLIT FILE INTO HEADER + CARD BLOCKS
# -----------------------------

def split_blocks(raw: str):
    lines = raw.splitlines()

    header = []
    blocks = []
    buf = []
    in_cards = False

    for line in lines:
        if line.startswith("card_"):
            in_cards = True
            if buf:
                blocks.append(buf)
                buf = []
            buf.append(line)
            continue

        if in_cards:
            buf.append(line)
        else:
            header.append(line)

    if buf:
        blocks.append(buf)

    return header, blocks


# -----------------------------
# EXTRACT NAME (TEXT SAFE)
# -----------------------------

def extract_name(block):
    for line in block:
        if "name:" in line:
            return line.split("name:", 1)[1].strip().strip('"').strip("'")
    return "unknown"


# -----------------------------
# INSERT NUMBER INTO FRONT (FIXED)
# -----------------------------

def insert_number_into_front(block, number):
    out = []

    in_front = False
    front_indent = None
    inserted = False

    next_indent = None

    for line in block:
        stripped = line.lstrip()

        # detect front start
        if stripped.startswith("front:"):
            in_front = True
            front_indent = len(line) - len(stripped)
            next_indent = front_indent + 2
            out.append(line)
            continue

        if in_front:
            # REMOVE existing number fields
            if stripped.startswith("number:"):
                continue

            # detect end of front block
            if stripped and not line.startswith(" " * next_indent) and ":" in stripped:
                if not inserted:
                    # REMOVE trailing blank lines before inserting number
                    while out and out[-1].strip() == "":
                        out.pop()

                    out.append(" " * next_indent + f"number: {number}")
                    inserted = True

                in_front = False

        out.append(line)

    # if front ends at EOF
    if in_front and not inserted:
        # REMOVE trailing blank lines before inserting number
        while out and out[-1].strip() == "":
            out.pop()

        out.append(" " * next_indent + f"number: {number}")

    return out


# -----------------------------
# PROCESS FILE (RENAME + SORT)
# -----------------------------

def process_file(path: Path):
    raw = path.read_text(encoding="utf-8").replace("\t", "  ")

    header, blocks = split_blocks(raw)

    seen = {}
    processed = []

    for block in blocks:
        name = extract_name(block)
        base = normalize_name(name)

        seen[base] = seen.get(base, 0) + 1
        key = f"card_{base}" if seen[base] == 1 else f"card_{base}_{seen[base]}"

        processed.append((key, block))

    processed.sort(key=lambda x: x[0])

    out = []
    out.extend(header)
    out.append("")

    for key, block in processed:
        out.append(key + ":")
        out.extend(block[1:])
        out.append("")

    path.write_text("\n".join(out), encoding="utf-8")

    print(f"✔ processed {path}")


# -----------------------------
# PROCESS FOLDER
# -----------------------------

def process_folder(root_folder: str):
    root = Path(root_folder)
    for file in root.rglob("*.yaml"):
        process_file(file)


# -----------------------------
# IMAGE RENAMER
# -----------------------------

def rename_images(root_folder: str):
    root = Path(root_folder)

    for p in root.rglob("*"):
        if not p.is_file():
            continue

        if p.suffix.lower() not in IMAGE_EXTS:
            continue

        old = p.stem
        new = normalize_name(old)

        if old == new:
            continue

        target = p.with_name(new + p.suffix)

        i = 1
        while target.exists():
            target = p.with_name(f"{new}_{i}{p.suffix}")
            i += 1

        print(f"{p} -> {target}")
        p.rename(target)


# -----------------------------
# RENUMBER BY FOLDER ORDER
# -----------------------------

def renumber_cards_by_explicit_folder_order(root_folder: str, folder_order: list[str]):
    root = Path(root_folder)
    counter = 1

    for folder_name in folder_order:
        folder = root / folder_name
        if not folder.exists():
            continue

        for file in sorted(folder.rglob("*.yaml")):
            raw = file.read_text(encoding="utf-8")

            header, blocks = split_blocks(raw)

            new_blocks = []

            for block in blocks:
                updated = insert_number_into_front(block, counter)
                counter += 1
                new_blocks.append(updated)

            out = []
            out.extend(header)
            out.append("")

            for b in new_blocks:
                out.extend(b)
                out.append("")

            file.write_text("\n".join(out), encoding="utf-8")

    return counter


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    root = "cards/_lck"

    process_folder(root)
    rename_images(root)
    renumber_cards_by_explicit_folder_order(root, CARD_ORDER)