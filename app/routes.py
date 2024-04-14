from flask import Flask, request, jsonify
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import torch

app = Flask(__name__)

# Cargar el modelo y el tokenizador
MODEL_NAME = "google-bert/bert-base-cased"
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Asegúrate de actualizar la ruta al modelo
MODEL_PATH = "./models/spam_classification_model.pth"
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

MODEL_PATH_RECOMMENDATIONS= "./models/recomendation.pth"
tokenizerRecomendation = AutoTokenizer.from_pretrained(MODEL_NAME)
modelRecomendation= AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
modelRecomendation.load_state_dict(torch.load(MODEL_PATH_RECOMMENDATIONS, map_location=torch.device('cpu')))
modelRecomendation.eval()


@app.route('/')
def home():
    return "Welcome to the spam classification API!"

@app.route('/classify', methods=['POST'])
def classify_text():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "No message provided for classification"}), 400

    # Tokenizar y preparar la entrada para el modelo
    inputs = tokenizer(message, padding=True, truncation=True, return_tensors="pt")

    # Predecir
    with torch.no_grad():
        logits = model(**inputs).logits

    # Convertir a probabilidades y obtener la clase predicha
    predicted_class = torch.argmax(logits, dim=-1).numpy().tolist()[0]
    
    # Puedes personalizar el retorno como desees
    classification = "spam" if predicted_class == 1 else "ham"
    return jsonify({"message": message, "classification": classification})

@app.route('/magic-conch', methods=['POST'])
def predict():
    data = request.get_json()
    sentence = data.get("sentence", "")

    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = modelRecomendation(**inputs)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1).numpy()
    classification = "positive" if predictions[0] == 1 else "negative"

    return jsonify({"sentence": sentence, "classification": classification})

@app.route('/zillow/api/v2/zgecon/type')
def get_data():
    response_data = {
        "success": True,
        "status": 200,
        "bundle": [
            {"values": [], "description": "For-sale Inventory", "key": "invt_fs", "metadataType": "metricType"},
            {"values": [], "description": "Mean Days to Pending", "key": "mean_doz_pending", "metadataType": "metricType"},
            {"values": [], "description": "Zillow Home Value Index", "key": "zhvi", "metadataType": "metricType"}
        ],
        "total": 15
    }
    return jsonify(response_data)

@app.route('/zillow/api/v2/zgecon/region')
def get_region_type():
    response_data = {
        "success": True,
        "status": 200,
        "bundle": [
            {"values": [], "description": "Country", "key": "1", "metadataType": "regionType"},
            {"values": [], "description": "Metro", "key": "14", "metadataType": "regionType"},
            {"values": [], "description": "State", "key": "2", "metadataType": "regionType"},
            {"values": [], "description": "County", "key": "4", "metadataType": "regionType"},
            {"values": [], "description": "City", "key": "6", "metadataType": "regionType"},
            {"values": [], "description": "Zip", "key": "7", "metadataType": "regionType"},
            {"values": [], "description": "Neighborhood", "key": "8", "metadataType": "regionType"}
        ],
        "total": 7
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)