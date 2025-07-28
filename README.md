# PDF Structure Extractor

A simple command‐line tool to extract a document title and structured outline (headings) from a PDF based purely on font‐size heuristics.

---

## 📝 Overview & Approach

1. **Font‐Size Frequency Analysis**  
   We scan every text span in each PDF page, rounding its font size to the nearest integer and counting how often each size occurs.

2. **Role Assignment with `get_font_roles()`**  
   - **Title Size**: the largest unique font size in the document  
   - **Body Size**: the most frequent font size, provided it exceeds an average‐count threshold  
   - **Heading Sizes**: any sizes larger than the body size but smaller than the title size

3. **Block Extraction & Filtering**  
   - Extract every text block (contiguous lines) along with its page number, bounding box, and list of spans.  
   - Reconstruct block text and discard empty or purely decorative blocks.

4. **Title Detection**  
   - On page 1, any block whose size matches `title_size` and is sufficiently long is treated as part of the document title.

5. **Heading Candidate Selection**  
   - Blocks whose size matches one of the `heading_sizes` and pass strict filters (e.g. not too long, not ending with “.” or “:”, not list items, not just numbers).

6. **Hierarchy Construction**  
   - Sort headings by their natural reading order (page & vertical position).  
   - Use a simple stack of font sizes to infer nesting depth: if a heading’s font size is smaller than the previous, it denotes a deeper level; if larger, it pops back up.

---

## 🛠️ Models & Libraries

- **[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)**  
  Used for PDF parsing and text/span extraction.
- **Python Standard Library**  
  - `collections.defaultdict`  
  - `re` (regular expressions)  
- **No external ML models** — purely rule‐based font‐size heuristics.

---

## 🚀 Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/your‑org/Adobe‑1A.git
   cd Adobe‑1A
