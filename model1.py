from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from asgiref.wsgi import WsgiToAsgi  # Convert Flask to ASGI

app = Flask(__name__)

# Load the trained model
model = load_model('model1/best_model.keras')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['data']
    data = np.array(data).reshape(1, 5, 1)  # Reshape for LSTM input
    prediction = model.predict(data).flatten().tolist()
    return jsonify({'prediction': prediction})

# Convert Flask (WSGI) to ASGI for Uvicorn compatibility
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=8001)
