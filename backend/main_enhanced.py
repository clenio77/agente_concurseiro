from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"])

@app.route('/health', methods=['GET', 'HEAD'])
def health_check():
    return jsonify({"status": "ok", "message": "Mentor de Concursos API funcionando"}), 200

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API funcionando corretamente"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
