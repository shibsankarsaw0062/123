# -*- coding: utf-8 -*-
"""Name_entity_recognization_last1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hyY_3mwuPXyJvJI5nZBV8doq_-kiqhcV

A Name entity recognition Approach To Detect Major
Feature In Legal Cases
"""

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

nlp = spacy.blank("en")
db = DocBin()

import json
f = open('/content/caseF2.json')
TRAIN_DATA = json.load(f)

TRAIN_DATA

import json
f = open('/content/caseT.json')
DEV_DATA = json.load(f)

DEV_DATA

for text, annot in tqdm(TRAIN_DATA['annotations']):
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

db.to_disk("./training_data.spacy")

for text, annot in tqdm(DEV_DATA['annotations']):
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

db.to_disk("./dev_data.spacy")

# Open the CFG file
with open('/content/base_config.cfg', 'r') as file:
    # Read and print each line
    for line in file:
        print(line.strip())  # Remove trailing newline characters

! python -m spacy init fill-config base_config.cfg config.cfg

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

! python -m spacy train config.cfg --output ./ --paths.train ./training_data.spacy --paths.dev ./dev_data.spacy

nlp_ner = spacy.load("/content/model-best")

pip install PyPDF2

import spacy
import PyPDF2
from spacy import displacy

# Load the SpaCy model from the custom path
nlp_ner = spacy.load("/content/model-best")

# PDF file path
pdf_path = '/content/case66.pdf'

# Open the PDF file
with open(pdf_path, 'rb') as pdf_file:
    # Create a PDF reader object
    reader = PyPDF2.PdfReader(pdf_file)

    # Initialize an empty string to store the output
    output_text = ""

    # Iterate through all pages
    for page_number in range(len(reader.pages)):
        # Extract text from the current page
        page_text = reader.pages[page_number].extract_text()

        # Process the text with the SpaCy model
        doc = nlp_ner(page_text)

        # Visualize named entities
        displacy.render(doc, style="ent", jupyter=True)

pip install WeasyPrint



import spacy
import PyPDF2
from spacy import displacy
from weasyprint import HTML

# Load the SpaCy model from the custom path
nlp_ner = spacy.load("/content/model-best")

# PDF file path
pdf_path = '/content/Paper18.pdf'

# Open the PDF file
with open(pdf_path, 'rb') as pdf_file:
    # Create a PDF reader object
    reader = PyPDF2.PdfReader(pdf_file)

    # Initialize an empty list to store the HTML strings for each page
    html_pages = []

    # Iterate through all pages
    for page_number in range(len(reader.pages)):
        # Extract text from the current page
        page_text = reader.pages[page_number].extract_text()

        # Process the text with the SpaCy model
        doc = nlp_ner(page_text)

        # Generate HTML for named entity visualization
        html = displacy.render(doc, style="ent", page=True, jupyter=False)

        # Append HTML for this page to the list
        html_pages.append(html)

# Combine HTML for all pages into a single HTML document
full_html = "\n".join(html_pages)

# Convert HTML to PDF
HTML(string=full_html).write_pdf("outputPaper18.pdf")

import matplotlib.pyplot as plt

# Data from the training logs
epochs = [0, 1, 2, 4, 7, 10, 14, 19, 25, 32, 42, 53, 66, 80, 94, 108, 122, 136, 150, 164, 178, 192, 206, 220, 234, 248, 262]
loss_tok2vec = [0.00, 272.48, 112.43, 463.89, 502.48, 655.86, 572.51, 712.97, 581.28, 249.65, 102.35, 134.17, 79.92, 258.82, 377.40, 76.79, 60.51, 240.49, 242.68, 80.68, 985.58, 300.89, 87.68, 44.82, 430.13, 361.07, 77.73]
loss_ner = [39.96, 2150.78, 1098.38, 1207.67, 1167.71, 1261.90, 1399.04, 794.35, 1132.82, 544.89, 236.56, 195.73, 142.05, 216.34, 167.77, 82.83, 57.67, 113.93, 155.52, 54.12, 216.10, 143.13, 58.00, 45.23, 148.39, 120.26, 47.89]

# Plotting
plt.figure(figsize=(10, 5))

# Loss plot
plt.subplot(1, 2, 1)
plt.plot(epochs, loss_tok2vec, label='Tok2Vec Loss', marker='o')
plt.plot(epochs, loss_ner, label='NER Loss', marker='o')
plt.title('Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# Accuracy plot
# Here, you need to have accuracy data for each epoch to plot accuracy.
# Assuming you have this data, replace the `accuracy` list with your actual accuracy values.
accuracy = [0.00, 0.49, 0.81, 0.76, 0.86, 0.84, 0.90, 0.91, 0.92, 0.92, 0.94, 0.94, 0.95, 0.94, 0.95, 0.95, 0.94, 0.94, 0.95, 0.94, 0.95, 0.94, 0.95, 0.94, 0.94, 0.95, 0.94]
plt.subplot(1, 2, 2)
plt.plot(epochs, accuracy, label='Accuracy', marker='o', color='green')
plt.title('Training Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()