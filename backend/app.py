from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os 

app = Flask(__name__)
CORS(app)  

# Cargar modelo
ruta_modelo = os.path.join(os.path.dirname(__file__), 'modelo_preguntas.pkl')
rf_model = joblib.load(ruta_modelo)

ruta_vectorizer = os.path.join(os.path.dirname(__file__), 'vectorizador.pkl')
vectorizer = joblib.load(ruta_vectorizer)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        pregunta = data.get('pregunta', '')
        
        # Vectorizar pregunta
        pregunta_vectorizada = vectorizer.transform([pregunta])
        
        # Predecir respuesta
        respuesta = rf_model.predict(pregunta_vectorizada)[0]
        
        return jsonify({'respuesta': respuesta})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error procesando la pregunta'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)