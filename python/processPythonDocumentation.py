import fitz  # PyMuPDF
import re
import spacy

# Open the PDF file
with fitz.open("python_library.pdf") as doc:
    text = ""
    start_page = 27 
    end_page = 2315
    for page_num in range(start_page, end_page + 1):
        # Extract text from each page
        page = doc.load_page(page_num)
        text += page.get_text()
        # print(page.get_text())

# text = text[140000:160000]

# Define a regex pattern for Python code blocks
code_pattern = re.compile(r'>>>.*?(\n|$)')
# Remove code blocks from the extracted text
text_without_code = re.sub(code_pattern, '', text)


# Load the language model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = len(text_without_code) + 10

# Process the cleaned text to segment into sentences
doc = nlp(text_without_code)
sentences = [sent.text.strip() for sent in doc.sents]

complex_pattern = re.compile(
    r"""
    # Match 'Chapter' followed by space(s) and number(s)
    ^.*?Chapter\s+\d+.*?$|
    # Match 'Release' followed by space(s) and version numbers
    ^.*?Release\s+\d+\.\d+\.\d+.*?$|
    # Match standalone page numbers
    ^\d+$|
    # Match standalone decorators like '@classmethod'
    ^\s*@[\w\.]+\s*$|
    # Match lines that consist solely of '...'
    ^\s*\.{3}\s*$|
    # Match function headers like 'def __dir__(self):', including those with ellipsis in the body
    ^\s*def\s+\w+\s*\(.*?\)\s*:\s*(?:\.\.\.|[^#])*?$|
    # Match simple return statements and other simple statements, possibly with ellipsis
    ^\s*(return|yield|pass)\s+[^#]+?(?:\.\.\.|[^#])*?$|
    # Match block of lines starting with a function call or an opening bracket
    ^\s*(?:\w+\s*\(.*?\)\s*|[\[\{]).*?(?:\.\.\.|[^#])*?$
    ^\s*$|
    """,
    re.MULTILINE | re.VERBOSE | re.DOTALL
)



# Assume sentences is a list of sentence strings
refined_sentences = []

def is_valid_sentence(sentence):
    # Define logic to determine if a sentence is coherent
    # For example, a coherent sentence should start with a capital letter and end with a terminal punctuation mark
    return len(sentence) > 0 and sentence[0].isupper() and sentence[-1] in '.?!'

for sentence in sentences:
    # Remove unwanted patterns from each sentence
    cleaned_sentence = re.sub(complex_pattern, '', sentence)
    
    # Check if the cleaned sentence is valid and not empty
    if is_valid_sentence(cleaned_sentence) and cleaned_sentence.strip():
        refined_sentences.append(cleaned_sentence.strip())


filename = 'python_refined_sentences.txt'
with open(filename, 'w', encoding='utf-8') as file:
    for sentence in refined_sentences:
        file.write(sentence + '\n')