#!/usr/bin/python

# PJS, 10/13/2017 
import base64
import codecs
import cStringIO
import io
import os
import PyPDF2
import re
import sys

# This script reads a document, looks for a Base64-encoded PDF,
# decodes it, and writes extracted PDF text to a file.
# The script uses PyPDF2 to extract text from de-encoded PDFs.
# Useful documentation for this library can be found at
# http://pythonhosted.org/PyPDF2/ and
# http://automatetheboringstuff.com/chapter13/.

# Regex for identifying and capturing Base64 with padding
b64Marker = '(^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$)'
# Regex for identifying and capturing PDF
pdfMarker = '(JVBERi0xLj.*)'
# Initialize variables for decoded PDF text and text 
# extracted from a decoded document
decodedText = ''
extractedText = ''

# Get filepath from user
filePath = raw_input('Path to file: ')
if os.path.isfile(filePath):
    print 'File exists: ' + str(os.path.isfile(filePath))
else:
    print 'File not found!'
    sys.exit()

# Read raw text from TDF document
f = open(filePath, 'r')
text = f.read()
f.close()

# Does the document contain Base64?
b64Hit = re.search(pdfMarker, text)
if b64Hit:
    print 'We have a b64Marker hit!'
    # Is the Base64 string an encoded PDF document?
    pdfHit = re.search(pdfMarker, b64Hit.group(1))
    if pdfHit:
        print 'We have a pdfMarker hit!'
        # Verify that the entire PDF document has been captured
        print 'START: ' + pdfHit.group(1)[0:100]
        print 'END: ' + pdfHit.group(1)[len(pdfHit.group(1)) - 100 : len(pdfHit.group(1))]
        # Decode Base64
        decodedText = base64.b64decode(pdfHit.group(1).strip())
        # PyPDF2 appears to want to work with a PDF file object,
        # so let's give it one
        pdfFileObj = cStringIO.StringIO()
        pdfFileObj.write(decodedText)
        # Create a PDF reader object from the PDF file object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # The reader appears to be able to retrieve single pages.
        # Since the reader itself is not iterable, we'll have to
        # settle for extracting text one page at a time. Pages are
        # zero-indexed, so the loop below will run from Page (0)
        # to Page (numPages-1).
        print 'This PDF has ' + str(pdfReader.numPages) + ' pages'
        for i in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            extractedText = extractedText + pageObj.extractText()
        # Write the extracted text to a file in UTF-8 format. Attempting to
        # write this text as ASCII will throw an error.
        try:
            new = codecs.open('./new.txt', 'w', 'utf8')
            new.write(extractedText)
            print 'Extracted text was successfully written to ./new.txt.'
        except IOError as e:
            print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
            print 'Extracted text was not written to an output file.'
        # Close all file objects
        new.close()
        pdfFileObj.close()
    else:
        print 'There\'s Base64 in here, but it doesn\'t appear to be a PDF.'
else:
    print 'Forget it, Jake. It\'s Chinatown.'

# End of script
