import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2
import spacy

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

nlp = spacy.load('en_core_web_sm')

data = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        if 'file[]' not in request.files:
            pass

        files = request.files.getlist("file[]")

        for file in files:
            if file.filename == '':
                break
        
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)

                with open(path, 'rb') as pdf:
                    reader = PyPDF2.PdfFileReader(pdf) 

                    keywords = set()
                    for page in reader.pages:
                        doc = nlp(page.extractText())
                        
                        for entity in doc.ents:
                            print(entity.text.lower() + ' ' + entity.label_)
                            keywords.add(entity.text.lower())

                    data.append((filename, keywords))

                os.remove(path)

        return render_template('uploads.html')
    else:
        return render_template('uploads.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        search_keyword = search.lower()
        results = []

        for title, keywords in data:
            if search_keyword in keywords:
                results.append(title)
                continue
        
        if search.strip() == '':
            search = None

        return render_template('index.html', search=search, results=results)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
