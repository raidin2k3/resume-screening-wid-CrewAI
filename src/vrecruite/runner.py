from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from main import run
import json
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mem = []

def output_txt():
    # Path to the file
    file_path = "/home/lestergreeks/Documents/codebase/proj/crewAI_demo/vrecruite/src/vrecruite/report.md"

    # Open and read the file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            contents = file.read()
            # print("Contents of report.md:\n")
            # print(contents)
        return contents
    except Exception as e:
        print(f"An error occurred: {e}")

def storage_clearance():
    folder = '/home/lestergreeks/Documents/codebase/proj/crewAI_demo/vrecruite/src/vrecruite/uploads'
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

@app.route('/api/resumeCatcher', methods=['POST'])
def upload_file():
    global mem
    try:

        # Log the request details
        print("Form data:", request.form)

        # Parse the uploaded file from the request
        files = request.files.getlist('files')  

        if not files or len(files) == 0:
            return jsonify({"message": "No files received."}), 400

        saved_files = []
        for file in files:
            if not file or file.filename == '':
                continue  # Skip empty files

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            saved_files.append(file.filename)
            
        ext = json.loads(request.form['job_details'])['requirements']
        words = re.findall(r'\b[a-zA-Z]+\b', ext)
        if mem!=words:
            with open("/home/lestergreeks/Documents/codebase/proj/crewAI_demo/vrecruite/src/vrecruite/report.md", "w") as f:
                f.write("")
        resl = output_txt()
        if resl:
            run(json.loads(request.form['job_details'])['requirements'],resl)
        else:
            run(json.loads(request.form['job_details'])['requirements'],None)
        mem = words
        # run(json.loads(request.form['job_details'])['requirements'])
        res = output_txt()
        storage_clearance()

        return jsonify({"message": "Files uploaded successfully.", 'results': res}), 200

    except Exception as e:
        return jsonify({"message": f"File upload failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=8000,debug=True)
