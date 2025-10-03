#!/bin/bash

echo "🔍 Verificando estrutura do projeto Mentor de Concursos..."

# Verificar se os arquivos principais existem
echo "📁 Verificando arquivos principais..."

if [ ! -f "backend/main_enhanced.py" ]; then
    echo "❌ backend/main_enhanced.py não encontrado"
    echo "📝 Criando arquivo principal do backend..."
    cat > backend/main_enhanced.py << 'EOF'
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
EOF
    echo "✅ backend/main_enhanced.py criado"
else
    echo "✅ backend/main_enhanced.py encontrado"
fi

if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ backend/requirements.txt não encontrado"
    echo "📝 Criando requirements.txt..."
    cat > backend/requirements.txt << 'EOF'
Flask==3.0.0
Flask-CORS==4.0.0
google-generativeai==0.3.2
PyPDF2==3.0.1
python-docx==1.1.0
firebase-admin==6.4.0
stripe==7.8.0
gunicorn==21.2.0
python-dotenv==1.0.0
requests==2.31.0
EOF
    echo "✅ backend/requirements.txt criado"
else
    echo "✅ backend/requirements.txt encontrado"
fi

if [ ! -f "frontend/package.json" ]; then
    echo "❌ frontend/package.json não encontrado"
    echo "📝 Criando package.json..."
    cat > frontend/package.json << 'EOF'
{
  "name": "mentor-concursos-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    "@types/node": "20.10.5",
    "@types/react": "18.2.45",
    "@types/react-dom": "18.2.18",
    "tailwindcss": "3.3.6",
    "autoprefixer": "10.4.16",
    "postcss": "8.4.32",
    "firebase": "10.7.1",
    "stripe": "14.9.0",
    "axios": "1.6.2"
  },
  "devDependencies": {
    "eslint": "8.56.0",
    "eslint-config-next": "14.0.4"
  }
}
EOF
    echo "✅ frontend/package.json criado"
else
    echo "✅ frontend/package.json encontrado"
fi

echo ""
echo "🎯 Estrutura verificada e arquivos essenciais criados!"
echo "📋 Próximos passos:"
echo "   1. Commit dos arquivos: git add . && git commit -m 'Add deploy configs'"
echo "   2. Push: git push origin main"
echo "   3. Deploy no Vercel/Netlify/Google Cloud Run"
