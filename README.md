# PDF Search with Gemini and ChromaDB

A Python example project that extracts text from PDFs, creates embeddings with Google's Gemini API, stores the text and embeddings in ChromaDB, and searches the policy document using cosine similarity.

## Features

- Extract PDF text page by page with PyMuPDF
- Split text into overlapping chunks
- Generate Gemini embeddings with retry and exponential backoff
- Store and update embeddings in a persistent ChromaDB collection
- Search a company policy and print the closest results with page numbers
- Generate sample policy and college PDFs

## Project Structure

| File | Description |
| --- | --- |
| `03_pdf_search.py` | PDF search exercise with TODO sections |
| `03_pdf_search_solution.py` | Completed PDF indexing and search implementation |
| `make_sample_pdf.py` | Generates `company_policy.pdf` |
| `create_pdf.py` | Generates `college_details.pdf` |
| `pdf_reader.py` | Simple PDF text-reading example |
| `company_policy.pdf` | Sample company policy |
| `college_details.pdf` | Sample college information |
| `resume.pdf` | Example resume PDF |
| `requirement.txt` | Python dependencies |
| `chroma_db/` | Persistent ChromaDB database |

## Prerequisites

- Python 3.10 or later
- A Google Gemini API key

## Installation

From the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirement.txt
```

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
EMBED_MODEL=gemini-embedding-001
```

`EMBED_MODEL` is optional and defaults to `gemini-embedding-001`.

## Usage

### Generate the sample policy PDF

```powershell
python make_sample_pdf.py
```

This creates `company_policy.pdf` with four pages of sample policy text.

### Run the PDF search

```powershell
python 03_pdf_search_solution.py
```

The completed script:

1. Opens the persistent ChromaDB database in `./chroma_db`
2. Reads and chunks `company_policy.pdf`
3. Creates Gemini embeddings for each chunk
4. Upserts the chunks into the `company_policy` collection
5. Runs several example policy questions
6. Prints the top matches, page numbers, cosine distances, and text previews

Run `03_pdf_search.py` only after completing its TODO sections.

### Read a PDF

`pdf_reader.py` demonstrates basic text extraction with PyPDF:

```powershell
python pdf_reader.py
```

Install PyPDF separately if it is not already available:

```powershell
python -m pip install pypdf
```

### Create the college PDF

```powershell
python create_pdf.py
```

Install ReportLab separately if it is not already available:

```powershell
python -m pip install reportlab
```

## Search Configuration

- Chunk size: 350 characters
- Chunk overlap: 70 characters
- Search metric: cosine similarity
- Default number of results: 3

Lower cosine distances indicate closer matches.

## Example Queries

- "When do I need a doctor's certificate for sick leave?"
- "How much can I claim for home internet and how often?"
- "What happens to unused annual leave at the end of the year?"
- "How quickly must I return my laptop after resigning?"
- "Are drinks or cigarettes covered during client travel meals?"

## Troubleshooting

**`Missing GEMINI_API_KEY in .env file.`**

Confirm that `.env` exists in the project root and contains a valid `GEMINI_API_KEY`.

**The PDF is not found**

Run the scripts from the project root so relative paths such as `company_policy.pdf` resolve correctly.

**The collection has old or unexpected data**

Delete the `chroma_db` directory and rerun `03_pdf_search_solution.py`. ChromaDB will create a fresh persistent database.
