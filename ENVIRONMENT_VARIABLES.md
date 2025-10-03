# 🔑 Variáveis de Ambiente - Mentor de Concursos

## Frontend (Vercel) - Variáveis Públicas

```bash
# API Backend
NEXT_PUBLIC_API_URL=https://mentor-concursos-backend.run.app

# Firebase (Configuração Pública)
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=mentor-concursos-xxx.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=mentor-concursos-xxx
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=mentor-concursos-xxx.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789012
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789012:web:abcdef1234567890

# Stripe (Chave Pública)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51234567890abcdef...

# Analytics (Opcional)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

## Backend (Google Cloud Run) - Variáveis Privadas

```bash
# 🚨 CRÍTICO: Gemini API
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Firebase Admin SDK (Serviço)
FIREBASE_PROJECT_ID=mentor-concursos-xxx
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@mentor-concursos-xxx.iam.gserviceaccount.com

# Stripe (Chaves Secretas)
STRIPE_SECRET_KEY=sk_test_51234567890abcdef...
STRIPE_WEBHOOK_SECRET=whsec_1234567890abcdef...

# Configurações do Servidor
FLASK_ENV=production
PORT=8080
CORS_ORIGINS=https://mentor-concursos.vercel.app
```

## 🔧 Como Configurar

### Vercel (Frontend):
1. Acesse o dashboard do projeto
2. Vá em Settings > Environment Variables
3. Adicione todas as variáveis `NEXT_PUBLIC_*`

### Google Cloud Run (Backend):
1. Acesse o Cloud Console
2. Vá em Cloud Run > Seu serviço > Edit & Deploy New Revision
3. Adicione todas as variáveis privadas

## 🚨 Variáveis OBRIGATÓRIAS para funcionamento:

### ✅ Frontend:
- `NEXT_PUBLIC_API_URL` - URL do backend
- `NEXT_PUBLIC_FIREBASE_*` - Configuração Firebase
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Pagamentos

### ✅ Backend:
- `GOOGLE_API_KEY` - **CRÍTICO** para LLM funcionar
- `FIREBASE_PROJECT_ID` - Banco de dados
- `FIREBASE_PRIVATE_KEY` - Autenticação admin
- `FIREBASE_CLIENT_EMAIL` - Serviço Firebase
- `STRIPE_SECRET_KEY` - Processar pagamentos

## 📋 Checklist de Deploy:

- [ ] Configurar Firebase Project
- [ ] Obter chave Gemini API
- [ ] Configurar Stripe Account
- [ ] Adicionar variáveis no Vercel
- [ ] Adicionar variáveis no Google Cloud Run
- [ ] Testar integração completa
