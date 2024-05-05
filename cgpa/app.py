from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import re
import json

app = Flask(__name__)

def extract_values_between_statements(pdf_text, start_statements, end_statements):
    values = []
    for start_statement, end_statement in zip(start_statements, end_statements):
        # Construct a regular expression pattern to find the substring between start_statement and end_statement
        pattern = re.escape(start_statement) + r'(.*?)' + re.escape(end_statement)

        # Find the match using the pattern
        match = re.search(pattern, pdf_text, re.DOTALL)

        # If match found, append the substring to the values list
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
    # Check if a file was uploaded
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    # Check if the file is a PDF
    if file.filename.endswith('.pdf'):
        try:
            # Read PDF content
            pdf = PdfReader(file)
            extracted_text = ''
            for page in pdf.pages:
                extracted_text += page.extract_text()

            # Define start and end statements for extraction
            start_statements = [
                "HS2121 Professional English and Functional skills",
                "MA2122 Calculus for Engineers",
                "PH2123 Engineering Physics",
                "CY2124 Engineering chemistry",
                "GE2125 Problem Solving and Python Programming",
                "GE2181 Problem Solving and Python Programming Laboratory",
                "BS2182 Physics and Chemistry Laboratory"
            ]
            end_statements = [
                "Semester",
                "Semester",
                "Semester",
                "Semester",
                "Semester",
                "Semester",
                "WD – With Drawn"
            ]

            # Extract values between statements
            values = extract_values_between_statements(extracted_text, start_statements, end_statements)

            # Convert the values to a JSON string
            values_json = json.dumps(values)

            return render_template('index.html', values_json=values_json)
        
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    else:
        return "Uploaded file is not a PDF", 400

if __name__ == '__main__':
    app.run(debug=True)
