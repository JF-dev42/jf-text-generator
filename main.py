from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_TOKEN = os.getenv("API_TOKEN")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=["POST"])
def generate():
    data = request.get_json()
    entrada = data.get("text", "")

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # Preparar el prompt
    estilo = "ensayo"
    texto = entrada

    if entrada.lower().startswith("tipo:"):
        try:
            partes = entrada.split(". Texto:")
            estilo = partes[0].replace("Tipo:", "").strip().lower()
            texto = partes[1].strip()
        except:
            pass

    prompt = (
        f"Respondé el siguiente texto con el estilo '{estilo}'. "
        "Usá un lenguaje claro, natural y humano. No repitas frases, y extendé la respuesta cuando sea posible. "
        f"Texto: {texto}"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.9,
            "top_p": 0.95,
            "max_new_tokens": 450,
            "repetition_penalty": 1.1
        }
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/bigscience/bloom",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        try:
            resultado = response.json()
            if isinstance(resultado, list) and "generated_text" in resultado[0]:
                return jsonify({"result": resultado[0]["generated_text"].replace(prompt, "").strip()})
            else:
                return jsonify({"result": "No se encontró el texto generado."})
        except Exception as e:
            return jsonify({"result": f"Error al procesar respuesta: {str(e)}"})
    else:
        return jsonify({"result": f"Error del modelo. Código: {response.status_code}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
