import difflib
from docx import Document as DocxDocument

def text_from_docx_filefield(filefield):
    text = ""
    doc = DocxDocument(filefield)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def generate_unified_diff(old_text, new_text):
    diff = difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        lineterm='',
        fromfile='old_version',
        tofile='new_version'
    )
    return "\n".join(diff)