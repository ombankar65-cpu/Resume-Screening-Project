from PyPDF2 import PdfReader

def get_pdf_text(pdf):

    text = ""

    reader = PdfReader(pdf)

    for page in reader.pages:

        text = text + page.extract_text()

    return text
