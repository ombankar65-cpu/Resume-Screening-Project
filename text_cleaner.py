import re

def clean_text(text):

    # lowercase
    text = text.lower()

    # remove numbers and symbols
    text = re.sub(r'[^a-zA-Z ]', '', text)

    return text
