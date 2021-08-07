from flask import Flask, request, render_template, jsonify
from word_suggest import last_word, reco

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict-word', methods=['POST'])
def predict_word():
    token = last_word(request.json['text'])
    recos = reco(token)
    
    return jsonify({
        'in': token,
        'out': recos[:10]
    })

app.run(debug= True)