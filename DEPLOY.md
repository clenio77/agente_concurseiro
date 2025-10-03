# Mentor de Concursos - Deploy Configuration

## 🚀 Estrutura do Projeto

```
mentor-concursos-app/
├── backend/                 # API Flask
│   ├── main_enhanced.py     # Servidor principal
│   ├── requirements.txt     # Dependências Python
│   ├── core/               # Lógica de negócio
│   └── api/                # Endpoints
├── frontend/               # Next.js App
│   ├── package.json        # Dependências Node.js
│   ├── next.config.mjs     # Configuração Next.js
│   └── src/                # Código fonte
├── vercel.json             # Configuração Vercel
├── netlify.toml            # Configuração Netlify
└── Dockerfile              # Configuração Docker
```

## 📋 Deploy Instructions

### Vercel (Frontend)
1. Conectar repositório GitHub
2. Configurar build: `frontend/`
3. Environment variables: `NEXT_PUBLIC_API_URL`

### Google Cloud Run (Backend)
1. Build Docker: `docker build -t mentor-concursos .`
2. Push: `gcloud run deploy --image gcr.io/PROJECT/mentor-concursos`
3. Environment variables: `GOOGLE_API_KEY`, `FIREBASE_CONFIG`

### Netlify (Frontend Alternativo)
1. Conectar repositório GitHub
2. Build settings: `frontend/`
3. Publish directory: `frontend/.next`

## 🔧 Environment Variables

### Backend
- `GOOGLE_API_KEY`: Chave da API Gemini
- `FIREBASE_CONFIG`: Configuração Firebase
- `STRIPE_SECRET_KEY`: Chave secreta Stripe

### Frontend
- `NEXT_PUBLIC_API_URL`: URL da API backend
- `NEXT_PUBLIC_FIREBASE_CONFIG`: Configuração Firebase
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Chave pública Stripe
