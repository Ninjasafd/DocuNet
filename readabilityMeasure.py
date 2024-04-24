import sys
from textatistic import Textatistic
import readability

def calculate_readability(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            text = file.read()
    
    results = readability.getmeasures(text, lang='en')
    return results['readability grades']

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a file path.")
    else:
        file_path = sys.argv[1]
        scores = calculate_readability(file_path)
        print(scores)
