import fitz  # PyMuPDF
import re
import spacy

# Open the PDF file
with fitz.open("gnu_cpp_documentation.pdf") as doc:
    text = ""
    start_page = 27 
    end_page = 308
    for page_num in range(start_page, end_page + 1):
        # Extract text from each page
        page = doc.load_page(page_num)
        text += page.get_text()



# Load the language model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = len(text) + 10

# Process the cleaned text to segment into sentences
doc = nlp(text)
sentences = [sent.text.strip() for sent in doc.sents]

code_pattern = re.compile(r"""
    (?s)                            # Dot matches newlines
    (?:                             # Non-capturing group for multiple patterns
        # Matches '#include <...>' and similar include statements
        #include\s*<.*?>|
        # Matches 'namespace {...}' blocks
        namespace\s*{.*?}|
        # Matches 'void functionName() {...}' blocks
        void\s*\w+\(\)\s*{.*?}|
        # Matches 'for (...) {...}' loops
        for\s*\(.*?\)\s*{.*?}|
        # Matches 'Chapter X' titles
        ^Chapter\s+\d+\s+.*?$|
        # Matches '8.1.1' headings
        ^\d+\.\d+(\.\d+)?\s+.*?$|
        # Matches 'The GNU C++ Library Manual X / Y'
        ^The\s+GNU\s+C\+\+\s+Library\s+Manual\s+\d+\s+/\s+\d+|
        # Matches tables like 'Name/Instantiating ... αmax = 1/2'
        Name/Instantiating.*?αmax\s+=\s+1/2\s*|
        # Matches templates and function definitions
        template\s*<.*?>.*?\{.*?\}|
        # Matches miscellaneous code snippets with braces
        \w+\s*\{.*?\}|
        # Matches section numbers followed by titles
        \d+\.\d+\.\d+\s+.*?
    )
""", re.MULTILINE | re.VERBOSE)





# Assume sentences is a list of sentence strings
refined_sentences = []

def is_valid_sentence(sentence):
    # Define logic to determine if a sentence is coherent
    # For example, a coherent sentence should start with a capital letter and end with a terminal punctuation mark
    return len(sentence) > 0 and sentence[0].isupper() and sentence[-1] in '.?!'

for sentence in sentences:
    # Remove unwanted patterns from each sentence
    cleaned_sentence = re.sub(code_pattern, '', sentence)
    
    # Check if the cleaned sentence is valid and not empty
    if is_valid_sentence(cleaned_sentence) and cleaned_sentence.strip():
        refined_sentences.append(cleaned_sentence.strip())


filename = 'cpp_refined_sentences.txt'
with open(filename, 'w', encoding='utf-8') as file:
    for sentence in refined_sentences:
        file.write(sentence + '\n')