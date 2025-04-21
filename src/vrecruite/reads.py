from PIL import Image
import pytesseract
import pdfplumber
import os

folder_path = "/home/lestergreeks/Documents/codebase/proj/crewAI_demo/vrecruite/src/vrecruite/resumes_for_eval"

def extract_text_from_scanned_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Convert the page to an image
            image = page.to_image().original
            text += pytesseract.image_to_string(image)
    return text

def process_files_in_folder(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        text_dict = {filename : ''}
        if os.path.isfile(file_path):  # Check if it's a file
            pdf_text = extract_text_from_scanned_pdf(file_path)
            text_dict[filename] = pdf_text
        texts.append(text_dict)
    return texts
        
