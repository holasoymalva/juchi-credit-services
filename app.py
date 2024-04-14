from flask import Flask, request, send_from_directory, jsonify, render_template, redirect
from flask_cors import CORS
import requests
import threading 
from pymessenger.bot import Bot

app = Flask(__name__, static_url_path='')
CORS(app)

VERIFY_TOKEN = "DEV-JUCHI"
ACCESS_TOKEN = ''

bot = Bot(ACCESS_TOKEN)

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


@app.route('/webviews/<path:path>')
def webviews(path):
    print('Ingrese')
    return send_from_directory('webviews', path)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, threaded=True)