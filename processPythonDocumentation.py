import fitz  # PyMuPDF
import re
import spacy

# Open the PDF file
with fitz.open("python_library.pdf") as doc:
    text = ""
    for page in doc:
        # Extract text from each page
        text += page.get_text()
        # print(page.get_text())


# Define a regex pattern for Python code blocks
code_pattern = re.compile(r'>>>.*?(\n|$)')

# Remove code blocks from the extracted text
text_without_code = re.sub(code_pattern, '', text)


# Load the language model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = len(text_without_code) + 100

# Process the cleaned text to segment into sentences
doc = nlp(text_without_code)
sentences = [sent.text.strip() for sent in doc.sents]

# Assume sentences is a list of sentence strings
refined_sentences = []

def is_coherent_sentence(sentence):
    # Define logic to determine if a sentence is coherent
    # For example, a coherent sentence should start with a capital letter and end with a terminal punctuation mark
    if sentence[0].isupper() and sentence.endswith(('.', '?', '!')):
        return True
    return False

for sentence in sentences:
    if is_coherent_sentence(sentence):
        refined_sentences.append(sentence)




filename = 'python_refined_sentences.txt'
with open(filename, 'w', encoding='utf-8') as file:
    for sentence in refined_sentences:
        file.write(sentence + '\n')