# analyzer/extract.py
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document

def extract_text(uploaded_file):
    """
    Extract text from an uploaded file (Streamlit UploadFile).
    Supports PDF and DOCX. Returns plain text (string).
    """
    if uploaded_file.type == "application/pdf":
        return pdf_extract_text(uploaded_file)
    elif uploaded_file.type in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    ):
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return ""
