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

### 🚨 CRÍTICO: Sem essas variáveis, o sistema não funciona!

### Backend (Google Cloud Run)
- `GOOGLE_API_KEY`: **OBRIGATÓRIO** - Chave da API Gemini para LLM
- `FIREBASE_PROJECT_ID`: ID do projeto Firebase
- `FIREBASE_PRIVATE_KEY`: Chave privada do Firebase Admin SDK
- `FIREBASE_CLIENT_EMAIL`: Email do serviço Firebase
- `STRIPE_SECRET_KEY`: Chave secreta Stripe para pagamentos
- `STRIPE_WEBHOOK_SECRET`: Webhook secret do Stripe
- `FLASK_ENV`: production
- `PORT`: 8080

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL`: URL da API backend
- `NEXT_PUBLIC_FIREBASE_API_KEY`: Chave pública Firebase
- `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`: Domínio de autenticação
- `NEXT_PUBLIC_FIREBASE_PROJECT_ID`: ID do projeto Firebase
- `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`: Bucket de storage
- `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`: Sender ID
- `NEXT_PUBLIC_FIREBASE_APP_ID`: App ID Firebase
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Chave pública Stripe

📋 **Ver arquivo completo:** `ENVIRONMENT_VARIABLES.md`
