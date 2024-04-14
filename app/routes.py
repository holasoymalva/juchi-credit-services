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

if __name__ == '__main__':
    app.run(debug=True)