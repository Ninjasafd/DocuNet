import re

# This regex pattern matches lines that start with >>> or ...
code_pattern = re.compile(r'^\s*(>>>|...).*$', re.MULTILINE)

# Sample text from the OCR process
sample_text = """
4.9.5 Memory Views
memoryview objects allow Python code to access the internal data of an object that supports the buffer protocol without copying.

class memoryview(object)
Create a memoryview that references object. object must support the buffer protocol. Built-in objects that support the buffer protocol include bytes and bytearray.

>>> v = memoryview(b'abcefg')
98
>>> v[1]
99
>>> v[-1]
103
>>> v[1:4]
memory at 0x7e3ddc9f4350>
>>> bytes(v[1:4])
b'bce'
"""

# Remove code samples
processed_text = re.sub(code_pattern, '', sample_text)

# Output the processed text
print(processed_text)


