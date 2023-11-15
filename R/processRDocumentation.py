import requests
from bs4 import BeautifulSoup
import re
import spacy

# URL of the 'An Introduction to R' manual
url = "https://cran.r-project.org/doc/manuals/r-release/R-intro.html"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all paragraph elements
paragraphs = soup.find_all('p')

# Initialize a list to hold all extracted text
all_text = []

# Loop over each paragraph and extract the text
for para in paragraphs:
    text = para.get_text()
    all_text.append(text.strip())

# Join all the paragraph texts into one large string
full_text = ' '.join(all_text)

text = ' '.join(all_text)

# Define a regex pattern for R code blocks
code_pattern = re.compile(r'>>>.*?(\n|$)')
# Remove code blocks from the extracted text
text_without_code = re.sub(code_pattern, '', text)

text = text_without_code
# Load the language model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = len(text) + 10

# Process the cleaned text to segment into sentences
doc = nlp(text)
sentences = [sent.text.strip() for sent in doc.sents]

regex_patterns = re.compile(
    r"""
    ^\d+(\.\d+)?\s+[\w\s]+$|
    ^\$\s+[\w\s]+$|
    ^>\s+[\w()]+$|
    ^(Next|Previous|Up):\s+[\w\s]+\(\[Contents\]\[Index\]\)$|
    ^\d+\s[\w\s;]+$|
    (^\d+(\.\d+)?\s+[\w\s]+$)|(^\$\s+[\w\s]+)|(^\>\s+[\w()]+)|(^(Next|Previous|Up):\s+[\w\s]+\(\[Contents\]\[Index\]\))|(^\d+\s[\w\s;]+)|
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
    cleaned_sentence = re.sub(regex_patterns, '', sentence)
    
    # Check if the cleaned sentence is valid and not empty
    if is_valid_sentence(sentence) and sentence.strip():
        refined_sentences.append(sentence.strip())


filename = 'R_refined_sentences.txt'
with open(filename, 'w', encoding='utf-8') as file:
    for sentence in refined_sentences:
        file.write(sentence + '\n')