from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
import re
import json

app = Flask(__name__)

def extract_values_between_statements(pdf_text, start_statements, end_statements):
    values = []
    for start_statement, end_statement in zip(start_statements, end_statements):
        pattern = re.escape(start_statement) + r'(.*?)' + re.escape(end_statement)
        match = re.search(pattern, pdf_text, re.DOTALL)
        if match:
            value = match.group(1).strip()
            values.append(value)
        else:
            values.append(None)
    return values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename.endswith('.pdf'):
        try:
            pdf = PdfReader(file)
            extracted_text = ''
            for page in pdf.pages:
                extracted_text += page.extract_text()

            start_statements = [
                "HS2121 Professional English and Functional skills",
                "MA2122 Calculus for Engineers",
                "PH2123 Engineering Physics",
                "CY2124 Engineering chemistry",
                "GE2125 Problem Solving and Python Programming",
                "Laboratory",
                "BS2182 Physics and Chemistry Laboratory"
            ]
            end_statements = [
                "Semester",
                "Semester",
                "Semester",
                "Semester",
                "Semester",
                "Semester",  # Using a regular expression to match a word boundary (space) as the end statement for GE2181
                "WD – With Drawn"  # Specific end statement for BS2182
            ]

            values = extract_values_between_statements(extracted_text, start_statements, end_statements)

            return jsonify(arrayOfArrays=[values])  # Send arrayOfArrays to the frontend as JSON
            
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    else:
        return "Uploaded file is not a PDF", 400

if __name__ == '__main__':
    app.run(debug=True)
