#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do Agente Concurseiro.
Cria todas as tabelas necessárias e dados iniciais.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def init_database():
    """Inicializa o banco de dados completo"""
    try:
        print("🔧 Inicializando banco de dados...")
        
        # Importar módulos necessários
        from app.db.base import Base, engine, SessionLocal
        from app.core.config import settings
        
        # Importar todos os modelos para garantir que sejam registrados
        print("📦 Importando modelos...")
        import app.db.models
        from app.db.models import User
        from app.core.security import get_password_hash
        
        # Criar diretório de dados se não existir
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        print(f"📁 Diretório de dados: {data_dir.absolute()}")
        
        # Criar todas as tabelas
        print("🏗️ Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Criar usuário admin inicial
        print("👤 Criando usuário administrador...")
        db = SessionLocal()
        try:
            # Verificar se já existe um usuário admin
            admin = db.query(User).filter(User.email == settings.FIRST_ADMIN_EMAIL).first()
            if admin:
                print("ℹ️ Usuário admin já existe")
            else:
                # Criar usuário admin
                admin_user = User(
                    email=settings.FIRST_ADMIN_EMAIL,
                    username=settings.FIRST_ADMIN_USERNAME,
                    password_hash=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
                    full_name="Administrador do Sistema",
                    is_active=True,
                )
                
                db.add(admin_user)
                db.commit()
                print("✅ Usuário admin criado com sucesso!")
                print(f"   Email: {settings.FIRST_ADMIN_EMAIL}")
                print(f"   Username: {settings.FIRST_ADMIN_USERNAME}")
                print(f"   Password: {settings.FIRST_ADMIN_PASSWORD}")
        finally:
            db.close()
        
        # Verificar tabelas criadas
        print("\n📊 Verificando tabelas criadas...")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        for table in sorted(tables):
            print(f"   ✅ {table}")
        
        print(f"\n🎉 Banco de dados inicializado com sucesso!")
        print(f"   📍 Localização: {settings.DATABASE_URL}")
        print(f"   📊 Total de tabelas: {len(tables)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
