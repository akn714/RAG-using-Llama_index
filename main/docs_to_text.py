import os
import textract
import PyPDF2
import python_pptx
import csv

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfFileReader(file)
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text
    # text = ""
    # with open(pdf_path, 'rb') as file:
    #     pdf_reader = PyPDF2.PdfFileReader(file)
    #     for page_num in range(pdf_reader.numPages):
    #         page = pdf_reader.getPage(page_num)
    #         text += page.extractText()
    # return text

def extract_text_from_docx(docx_path):
    text = ""
    doc = python_pptx.Document(docx_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def extract_text_from_pptx(pptx_path):
    text = ""
    prs = python_pptx.Presentation(pptx_path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + '\n'
    return text

def extract_text_from_document(document_path):
    _, file_extension = os.path.splitext(document_path)
    file_extension = file_extension.lower()
    if file_extension == '.pdf':
        return extract_text_from_pdf(document_path)
    elif file_extension in ('.docx', '.doc'):
        return extract_text_from_docx(document_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(document_path)
    elif file_extension == '.pptx':
        return extract_text_from_pptx(document_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return ""

def extract_text_from_csv(csv_path, column_name):
    text = ""
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if column_name in row:
                text += row[column_name] + '\n'
    return text

# Example usage:
pdf_text = extract_text_from_pdf('example.pdf')
docx_text = extract_text_from_docx('example.docx')
txt_text = extract_text_from_txt('example.txt')
pptx_text = extract_text_from_pptx('example.pptx')
csv_text = extract_text_from_csv('example.csv', 'text_column_name')

print("PDF Text:")
print(pdf_text)
print("\nDOCX Text:")
print(docx_text)
print("\nTXT Text:")
print(txt_text)
print("\nPPTX Text:")
print(pptx_text)
print("\nCSV Text:")
print(csv_text)



