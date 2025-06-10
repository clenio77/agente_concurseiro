# Dockerfile para Agente Concurseiro
FROM python:3.11-slim

# Metadados
LABEL maintainer="Agente Concurseiro Team"
LABEL version="2.0.0"
LABEL description="Sistema completo de preparação para concursos públicos"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production
ENV PORT=8000

# Criar usuário não-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .
COPY requirements-prod.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p data/users data/questions data/dashboard backups logs config

# Definir permissões
RUN chown -R appuser:appuser /app
RUN chmod +x scripts/entrypoint.sh

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Comando de entrada
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
