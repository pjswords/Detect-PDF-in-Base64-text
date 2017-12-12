File pdf-from-b64-py2.py works with Python 2, and file pdf-from-b64-py3.py works with Python 3. Both scripts perform the same function.

Each script reads a document, looks for a Base64-encoded PDF, decodes it, and writes extracted PDF text to a file. The scripts use the PyPDF2 library to extract text from de-encoded PDFs.
