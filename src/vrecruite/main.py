#!/usr/bin/env python
import sys
import warnings
from vrecruite.crew import Vrecruite
# from googleapiclient.discovery import build
# from google.oauth2.service_account import Credentials
# from googleapiclient.http import MediaIoBaseDownload
import io
import pdfplumber
import pytesseract
import os
from docx import Document

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")



# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(reqs, history=None):
    docs = drive_intgr8()
    
    if docs is None:
        return "Feed me some resume(s)!"
    
    inputs = {
        'link': docs,
        'requirements': reqs,
        'past': history if history else None
    }

    try:
        Vrecruite().crew().kickoff(inputs=inputs)
        if history:
            print(history)
    except Exception as e:
        print(e)
        raise Exception(f"An error occurred while replaying the crew: {e}")



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Vrecruite().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Vrecruite().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Vrecruite().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


##################################################################################################################################################

def drive_intgr8():

    # Path to your service account key file
    # SERVICE_ACCOUNT_FILE = ''
    # SCOPES = ['']

    # Authenticate using the service account
    # credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # service = build('drive', 'v3', credentials=credentials)
    
    FOLDER_ID = '/home/lestergreeks/Documents/codebase/proj/crewAI_demo/vrecruite/src/vrecruite/uploads'
    # FOLDER_ID = ''

    # Function to list files in a Google Drive folder
    def list_files_in_folder(folder_path):
        try:
            files = [
                {"name": f, "path": os.path.join(folder_path, f)}
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
            ]
            return files
        except FileNotFoundError:
            # print(f"Folder not found: {folder_path}")
            return []

    # Function to read file content as a byte stream
    def read_file_from_folder(file_path):
        try:
            with open(file_path, "rb") as file:
                file_stream = io.BytesIO(file.read())
                file_stream.seek(0)  # Reset the stream's pointer to the beginning
                return file_stream
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
    
    def extract_text_from_scanned_pdf(file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Convert the page to an image
                image = page.to_image().original
                text += pytesseract.image_to_string(image)
        return text
    
    def read_docx(path):
        document = Document(path)

        full_text = ""
        for paragraph in document.paragraphs:
            full_text += paragraph.text
        full_text = "\n".join(full_text)
        return full_text
    
    # Function to extract text from files in a Google Drive folder
    def process_files_in_folder(folder_path):
        texts = ""
        files = list_files_in_folder(folder_path)

        for file in files:
            file_name = file['name']
            file_path = file['path']
            print(file_path)

            try:
                # Read the file as a byte stream
                with open(file_path, 'rb') as file_stream:
                    text_dict = ""
                    # Process the file (Assume `extract_text_from_scanned_pdf` can accept a byte stream)
                    if ".docx" in file_name:
                        doc_text = read_docx(file_path)
                        text_dict += doc_text

                    else:
                        pdf_text = extract_text_from_scanned_pdf(file_stream)
                        text_dict += pdf_text
                    texts += text_dict
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

        if not texts:
            return None

        return texts

    return process_files_in_folder(FOLDER_ID) 
