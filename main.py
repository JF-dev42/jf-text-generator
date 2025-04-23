from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_TOKEN = os.getenv("API_TOKEN")

def generar_respuesta(texto):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    data = {
        "inputs": texto,
        "parameters": {
            "temperature": 0.7,         # Más natural
            "top_p": 0.9,               # Equilibrado
            "max_new_tokens": 400,      # Ensayos más largos
            "repetition_penalty": 1.1   # Menos repeticiones
        }
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        try:
            resultado = response.json()
            if isinstance(resultado, list) and "generated_text" in resultado[0]:
                return resultado[0]["generated_text"]
            else:
                return "No se encontró el texto generado."
        except Exception as e:
            return f"Error al procesar respuesta: {str(e)}"
    else:
        return f"Error al generar respuesta. Código: {response.status_code}"

@app.route('/', methods=["GET", "POST"])
def home():
    respuesta = ""
    if request.method == "POST":
        texto = request.form["texto"]
        respuesta = generar_respuesta(texto)
    return render_template("index.html", respuesta=respuesta)

app.run(host="0.0.0.0", port=81)
