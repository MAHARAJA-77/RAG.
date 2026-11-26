
from pypdf import PdfReader

# Open PDF file
reader = PdfReader("resume.pdf")

# Read all pages
for page_number, page in enumerate(reader.pages):
    text = page.extract_text()

    print(f"Page {page_number + 1}")
    print(text)
