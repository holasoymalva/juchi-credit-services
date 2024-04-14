from flask import Flask, request, send_from_directory, jsonify, render_template, redirect
from flask_cors import CORS
import requests
import threading 
import pdfplumber
import pytesseract
from PIL import Image
import io
from pymessenger.bot import Bot

app = Flask(__name__, static_url_path='')
CORS(app)

VERIFY_TOKEN = "DEV-JUCHI"
ACCESS_TOKEN = ''

bot = Bot(ACCESS_TOKEN)

properties = [
    {"id": 1, "type": "rent", "price": 800, "location": "Ciudad de México", "credit_score_required": 600},
    {"id": 2, "type": "buy", "price": 150000, "location": "Guadalajara", "credit_score_required": 700},
    {"id": 3, "type": "rent", "price": 500, "location": "Monterrey", "credit_score_required": 550},
    {"id": 4, "type": "buy", "price": 200000, "location": "Ciudad de México", "credit_score_required": 750},
    {"id": 5, "type": "rent", "price": 1000, "location": "Cancún", "credit_score_required": 650}
]


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test',methods=['GET'])
def hello_tets():
    jsonTest = {
        "codigoOperacion": 0,
        "datosSalida":"",
        "detalleMensaje": "El test Funciona de manera adecuada.",
        "mensaje": '',
        "tipoMensaje": "Operacion Exitosa",
    }
    return jsonTest

@app.route('/webhooknew', methods=['GET', 'POST'])
def webhook():
    print("LLego peticion...")
    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            try:
                messaging = event['messaging']
                for eventMessage in messaging:
                    recipient_id = eventMessage['sender']['id']
                    analitycs_id = eventMessage['recipient']['id']
                    global senderID
                    senderID = eventMessage
                    t = c(target=process, args=(eventMessage, recipient_id, analitycs_id, ora,))
                    t.start()
                    print("Return 200",eventMessage)
                    return "prueba de 200", 200
                    #procesamiento(eventMessage,recipient_id, analitycs_id, ora)
            except Exception as e:
                print("webhook",e)
                return "prueba de 200", 200
    elif request.method == 'GET':
        print(VERIFY_TOKEN)
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        print("Return 200 1")
        return "Verificar el token", 200
    print("Return 200 2")
    return "Chatbot Grupo Salinas", 200

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Get credit score from request
    data = request.get_json()
    credit_score = data.get('credit_score')
    if credit_score is None:
        return jsonify({"error": "Credit score is required"}), 400

    # Filter properties that match the credit score
    recommended_properties = [prop for prop in properties if prop['credit_score_required'] <= credit_score]

    return jsonify(recommended_properties)

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        content = extract_text_from_pdf(file)
        credit_score = calculate_credit_score(content)
        return jsonify({'message': 'PDF processed', 'credit_score': credit_score}), 200

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        pages = pdf.pages
        full_text = ''
        for page in pages:
            full_text += page.extract_text()
    return full_text

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        credit_score = calculate_credit_score(text)
        return jsonify({'message': 'File successfully processed', 'credit_score': credit_score}), 200


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def calculate_credit_score(text):
    # Implementa tu lógica para calcular el score crediticio
    return "Score based on OCR text"
    
@app.route('/webviews/<path:path>')
def webviews(path):
    print('Ingrese')
    return send_from_directory('webviews', path)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, threaded=True)