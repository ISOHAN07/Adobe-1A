import fitz  # PyMuPDF
from collections import defaultdict
import re

def get_font_roles(font_counts: defaultdict, threshold_multiplier: float = 2.0) -> dict:
    """
    Determines font size roles: title, headings, body based on frequency.
    """
    if not font_counts:
        return {}

    total_occurrences = sum(font_counts.values())
    average_count = total_occurrences / len(font_counts)
    body_threshold = average_count * threshold_multiplier

    sorted_by_count = sorted(font_counts.items(), key=lambda item: item[1], reverse=True)
    body_size = sorted_by_count[0][0] if sorted_by_count[0][1] > body_threshold else 0

    sorted_sizes = sorted(font_counts.keys(), reverse=True)
    title_size = sorted_sizes[0] if sorted_sizes else 0

    heading_sizes = [
        size for size in sorted_sizes
        if size > body_size and size != title_size
    ]

    return {
        "title_size": title_size,
        "heading_sizes": sorted(heading_sizes, reverse=True),
        "body_size": body_size
    }

def extract_pdf_structure(pdf_path: str) -> dict:
    """
    Extracts document structure using only font sizes.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return {"error": f"Failed to open PDF: {e}"}

    if doc.page_count > 50:
        return {"error": "PDF exceeds the 50-page limit."}

    font_counts = defaultdict(int)
    all_blocks = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT, sort=True)["blocks"]
        for block in blocks:
            if not block.get("lines") or not block["lines"][0].get("spans"):
                continue

            block_lines = block["lines"]
            for line in block_lines:
                for span in line["spans"]:
                    font_size = round(span["size"])
                    font_counts[font_size] += 1

            all_blocks.append({
                "page": page_num + 1,
                "bbox": block["bbox"],
                "lines": block_lines
            })

    if not font_counts:
        return {"title": "Empty Document", "outline": []}

    font_roles = get_font_roles(font_counts)
    title_size = font_roles.get("title_size", 0)
    heading_sizes = font_roles.get("heading_sizes", [])

    title_texts = []
    heading_candidates = []

    for item in all_blocks:
        text = " ".join(
            "".join(span["text"] for span in line["spans"]).strip()
            for line in item["lines"]
        ).strip().replace("  ", " ")

        if not text:
            continue

        block_font_size = round(item["lines"][0]["spans"][0]["size"])

        # Title detection
        if item["page"] == 1 and block_font_size == title_size:
            if len(text) > 15:
                title_texts.append(text)
            continue

        # Heading detection
        if block_font_size in heading_sizes:
            if len(item["lines"]) > 3 or text.endswith(('.', ':')): continue
            if len(text) < 3 or text.isdigit(): continue
            if re.match(r'^\d+\.\s*|\([a-z0-9]+\)|\•|\-|[A-Z]\.\s', text): continue

            heading_candidates.append({
                "text": text,
                "font_size": block_font_size,
                "page": item["page"],
                "y": item["bbox"][1]
            })

    title = " ".join(title_texts) if title_texts else "Untitled Document"

    # Build outline hierarchy
    outline = []
    size_stack = []

    for heading in heading_candidates:
        size = heading["font_size"]

        while size_stack and size > size_stack[-1]:
            size_stack.pop()

        if not size_stack or size < size_stack[-1]:
            size_stack.append(size)

        level = len(size_stack)
        if level > 4: level = 4

        outline.append({
            "level": f"H{level}",
            "text": heading["text"],
            "page": heading["page"]
        })

    doc.close()
    return {
        "title": title,
        "outline": outline
    }
