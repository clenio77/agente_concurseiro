# 🚀 Deploy no Vercel - Agente Concurseiro

## 📋 Pré-requisitos

### 1. **Configurar Variáveis de Ambiente no Vercel:**

Acesse o dashboard do Vercel e configure as seguintes variáveis:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://seu-projeto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua_chave_anonima_aqui
SUPABASE_SERVICE_ROLE_KEY=sua_chave_service_role_aqui

# NextAuth
NEXTAUTH_SECRET=seu_secret_aqui_min_32_caracteres
NEXTAUTH_URL=https://seu-dominio.vercel.app

# Ambiente
NODE_ENV=production
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_APP_URL=https://seu-dominio.vercel.app
```

### 2. **Configurar no Dashboard do Vercel:**

1. Acesse: `https://vercel.com/dashboard`
2. Selecione seu projeto
3. Vá em **Settings** → **Environment Variables**
4. Adicione cada variável acima

## 🔧 Configuração Automática

O arquivo `vercel.json` já está configurado para usar as variáveis de ambiente.

## 🚀 Deploy

1. **Push para main** - Deploy automático
2. **Verificar logs** - Monitorar build
3. **Testar funcionalidades** - Validar produção

## ⚠️ Observações

- **Variáveis de ambiente** são obrigatórias para funcionalidades completas
- **Valores padrão** são usados apenas para build (não para funcionalidade)
- **Supabase** deve estar configurado e funcionando
