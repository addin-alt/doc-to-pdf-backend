from flask import Flask, request, send_file
import subprocess
import os
import uuid
import platform

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# LibreOffice path: Mac uses full path, Linux uses 'soffice'
if platform.system() == "Darwin":  # macOS
    LIBREOFFICE_PATH = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
else:  # Linux
    LIBREOFFICE_PATH = "soffice"

@app.route("/convert", methods=["POST"])
def convert():
    # Check if file is uploaded
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    # Validate file type
    if not file.filename.lower().endswith((".docx", ".doc")):
        return "Invalid file type. Please upload DOCX or DOC.", 400

    # Save file with unique name
    unique_name = f"{uuid.uuid4()}.docx"
    doc_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(doc_path)

    # Convert DOCX → PDF using LibreOffice
    try:
        subprocess.run([
            LIBREOFFICE_PATH,
            "--headless",
            "--convert-to", "pdf",
            doc_path,
            "--outdir", UPLOAD_FOLDER
        ], check=True)
    except subprocess.CalledProcessError:
        return "Conversion failed", 500

    # Send PDF back
    pdf_path = doc_path.replace(".docx", ".pdf")
    if not os.path.exists(pdf_path):
        return "PDF not found after conversion", 500

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
