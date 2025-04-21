from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
import pdfplumber
import pytesseract

def gdrive_intgr8():

    # Path to your service account key file
    SERVICE_ACCOUNT_FILE = ''
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    FOLDER_ID = ''

    # Authenticate using the service account
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    # Function to list files in a Google Drive folder
    def list_files_in_drive_folder(folder_id):
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])

    # Function to read file content as a byte stream
    def read_file_from_drive(file_id):
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        file_stream.seek(0)  # Reset the stream's pointer to the beginning
        return file_stream
    
    def extract_text_from_scanned_pdf(file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Convert the page to an image
                image = page.to_image().original
                text += pytesseract.image_to_string(image)
        return text

    # Function to extract text from files in a Google Drive folder
    def process_files_in_google_drive_folder(folder_id):
        texts = []
        files = list_files_in_drive_folder(folder_id)

        for file in files:
            file_name = file['name']
            file_id = file['id']

            # Read the file as a byte stream
            file_stream = read_file_from_drive(file_id)
            try:
                # Process the file (Assume `extract_text_from_scanned_pdf` can accept a byte stream)
                pdf_text = extract_text_from_scanned_pdf(file_stream)
                text_dict = {file_name: pdf_text}
                texts.append(text_dict)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

        return texts

    return process_files_in_google_drive_folder(FOLDER_ID) 

# print(gdrive_intgr8())