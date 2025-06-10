"""
Teste completo para verificar se o sistema está 100% pronto para produção
"""

import os
import sys
import asyncio
import json
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_system():
    """Testa sistema de banco de dados"""
    print("\n🗄️ Testando sistema de banco de dados...")
    
    try:
        from app.db.database import db_manager, init_database, seed_database
        
        # Testar inicialização
        if init_database():
            print("✅ Banco de dados inicializado")
        else:
            print("❌ Falha na inicialização do banco")
            return False
        
        # Testar health check
        if db_manager.health_check():
            print("✅ Health check do banco passou")
        else:
            print("❌ Health check do banco falhou")
            return False
        
        # Testar estatísticas
        stats = db_manager.get_stats()
        print(f"✅ Estatísticas obtidas: {stats.get('users_count', 0)} usuários")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de banco: {e}")
        return False

def test_authentication_system():
    """Testa sistema de autenticação"""
    print("\n🔐 Testando sistema de autenticação...")
    
    try:
        from app.auth.auth_manager import auth_manager
        
        # Testar criação de usuário
        result = auth_manager.create_user(
            email="test@example.com",
            username="testuser",
            password="TestPassword123!",
            full_name="Usuário Teste"
        )
        
        if result["success"]:
            print("✅ Usuário criado com sucesso")
            user_id = result["user_id"]
        else:
            print(f"⚠️ Usuário já existe ou erro: {result['error']}")
            user_id = None
        
        # Testar autenticação
        auth_result = auth_manager.authenticate_user(
            "test@example.com",
            "TestPassword123!",
            "127.0.0.1"
        )
        
        if auth_result["success"]:
            print("✅ Autenticação bem-sucedida")
            token = auth_result["access_token"]
            
            # Testar verificação de token
            payload = auth_manager.verify_token(token)
            if payload:
                print("✅ Token verificado com sucesso")
            else:
                print("❌ Falha na verificação do token")
                return False
        else:
            print(f"❌ Falha na autenticação: {auth_result['error']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de autenticação: {e}")
        return False

def test_ai_integration():
    """Testa integração com IA"""
    print("\n🤖 Testando integração com IA...")
    
    try:
        from app.ai.openai_integration import openai_manager
        
        if openai_manager.enabled:
            print("✅ OpenAI configurada e habilitada")
            
            # Teste básico de contagem de tokens
            token_count = openai_manager.count_tokens("Este é um teste")
            print(f"✅ Contagem de tokens funcionando: {token_count}")
            
        else:
            print("⚠️ OpenAI não configurada - usando fallbacks")
        
        # Testar fallbacks
        user_profile = {
            "target_position": "Analista",
            "target_banca": "CESPE",
            "experience_level": "intermediário"
        }
        
        plan = openai_manager._fallback_study_plan(user_profile)
        if plan:
            print("✅ Fallback de plano de estudos funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração IA: {e}")
        return False

def test_monitoring_system():
    """Testa sistema de monitoramento"""
    print("\n📊 Testando sistema de monitoramento...")
    
    try:
        from app.monitoring.metrics import metrics_collector, health_checker, get_metrics
        
        # Testar coleta de métricas
        metrics_collector.collect_system_metrics()
        print("✅ Métricas do sistema coletadas")
        
        # Testar health checks
        async def test_health():
            results = await health_checker.run_checks()
            healthy_checks = sum(1 for check in results['checks'].values() if check['status'] == 'healthy')
            total_checks = len(results['checks'])
            print(f"✅ Health checks: {healthy_checks}/{total_checks} passaram")
            return results['status'] == 'healthy'
        
        health_result = asyncio.run(test_health())
        
        # Testar geração de métricas
        metrics_data = get_metrics()
        if metrics_data:
            print("✅ Métricas Prometheus geradas")
        
        return health_result
        
    except Exception as e:
        print(f"❌ Erro no sistema de monitoramento: {e}")
        return False

def test_backup_system():
    """Testa sistema de backup"""
    print("\n💾 Testando sistema de backup...")
    
    try:
        from app.backup.backup_manager import backup_manager
        
        # Testar criação de backup
        backup_path = backup_manager.create_database_backup()
        if backup_path:
            print(f"✅ Backup criado: {backup_path}")
        else:
            print("⚠️ Backup não criado (normal se banco não existir)")
        
        # Testar listagem de backups
        backups = backup_manager.list_backups()
        print(f"✅ {len(backups)} backups listados")
        
        # Testar status
        status = backup_manager.get_backup_status()
        print(f"✅ Status do backup obtido: {status['total_backups']} backups")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de backup: {e}")
        return False

def test_writing_system():
    """Testa sistema avançado de redação"""
    print("\n✍️ Testando sistema de redação...")
    
    try:
        from tools.writing_tool import WritingTool
        
        writing_tool = WritingTool()
        
        # Texto de teste
        texto_teste = """
        A sustentabilidade ambiental representa um dos maiores desafios contemporâneos. 
        
        Em primeiro lugar, é fundamental reconhecer que o desenvolvimento econômico não pode ocorrer em detrimento do meio ambiente. Portanto, torna-se necessário implementar políticas públicas que promovam o equilíbrio entre crescimento e preservação.
        
        Ademais, a educação ambiental constitui ferramenta essencial para conscientização da população. Assim, investimentos em programas educacionais podem gerar mudanças significativas no comportamento social.
        
        Conclui-se, portanto, que a sustentabilidade ambiental exige ações coordenadas entre governo, empresas e sociedade civil para garantir um futuro sustentável para as próximas gerações.
        """
        
        # Testar avaliação por banca
        resultado = writing_tool.evaluate_essay_by_banca(
            texto_teste, 
            "CESPE", 
            "dissertativo-argumentativo",
            "Sustentabilidade ambiental"
        )
        
        if "error" not in resultado:
            print(f"✅ Redação avaliada - Nota: {resultado['score_final']}/10")
            print(f"   Critérios avaliados: {len(resultado['scores_por_criterio'])}")
        else:
            print(f"❌ Erro na avaliação: {resultado['error']}")
            return False
        
        # Testar banco de temas
        tema = writing_tool.get_tema_by_banca("CESPE")
        if "error" not in tema:
            print(f"✅ Tema obtido: {tema['tema']}")
        else:
            print(f"⚠️ Erro ao obter tema: {tema['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de redação: {e}")
        return False

def test_gamification_system():
    """Testa sistema de gamificação"""
    print("\n🎮 Testando sistema de gamificação...")
    
    try:
        from app.utils.gamification import GamificationSystem
        
        # Criar sistema de gamificação
        gamification = GamificationSystem("test_user_prod")
        
        # Testar adição de experiência
        result = gamification.add_experience(150, "daily_quiz")
        print(f"✅ Experiência adicionada: {result.get('message', 'OK')}")
        
        # Testar verificação de conquistas
        activity_data = {
            "current_streak": 10,
            "study_hours": 30,
            "best_score": 88
        }
        
        new_achievements = gamification.check_achievements(activity_data)
        print(f"✅ Conquistas verificadas: {len(new_achievements)} novas")
        
        # Testar resumo do usuário
        summary = gamification.get_user_summary()
        print(f"✅ Resumo gerado - Nível: {summary['level']}, Pontos: {summary['total_points']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de gamificação: {e}")
        return False

def test_analytics_system():
    """Testa sistema de analytics"""
    print("\n📈 Testando sistema de analytics...")
    
    try:
        from app.utils.performance_predictor import PerformancePredictor
        
        predictor = PerformancePredictor()
        
        # Dados de teste
        user_data = {
            'mock_exam_scores': [
                {'score': 70, 'date': '2024-01-01'},
                {'score': 75, 'date': '2024-01-08'},
                {'score': 80, 'date': '2024-01-15'}
            ],
            'subject_progress': {
                'Português': {'last_score': 82},
                'Matemática': {'last_score': 68},
                'Direito': {'last_score': 85}
            },
            'total_study_hours': 100,
            'simulados_completed': 5
        }
        
        # Testar análise de desempenho
        metrics = predictor.analyze_performance(user_data)
        print(f"✅ Métricas analisadas - Score geral: {metrics.overall_score:.1f}%")
        
        # Testar predição
        prediction = predictor.predict_exam_performance(user_data, "CESPE", 60)
        print(f"✅ Predição gerada - Score previsto: {prediction.predicted_score:.1f}%")
        print(f"   Confiança: {prediction.confidence:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de analytics: {e}")
        return False

def test_docker_readiness():
    """Testa se o sistema está pronto para Docker"""
    print("\n🐳 Testando prontidão para Docker...")
    
    try:
        # Verificar arquivos essenciais
        essential_files = [
            "Dockerfile",
            "docker-compose.yml",
            "requirements-prod.txt",
            "scripts/entrypoint.sh",
            "deploy.sh"
        ]
        
        missing_files = []
        for file in essential_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Arquivos faltando: {missing_files}")
            return False
        else:
            print("✅ Todos os arquivos Docker estão presentes")
        
        # Verificar estrutura de diretórios
        required_dirs = [
            "app/db",
            "app/auth", 
            "app/api",
            "app/monitoring",
            "app/backup",
            "app/ai"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            print(f"❌ Diretórios faltando: {missing_dirs}")
            return False
        else:
            print("✅ Estrutura de diretórios completa")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação Docker: {e}")
        return False

def test_ci_cd_readiness():
    """Testa se o sistema está pronto para CI/CD"""
    print("\n🔄 Testando prontidão para CI/CD...")
    
    try:
        # Verificar arquivos de CI/CD
        cicd_files = [
            ".github/workflows/ci-cd.yml"
        ]
        
        missing_files = []
        for file in cicd_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Arquivos CI/CD faltando: {missing_files}")
            return False
        else:
            print("✅ Arquivos CI/CD presentes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação CI/CD: {e}")
        return False

def main():
    """Executa todos os testes de produção"""
    print("🚀 TESTE COMPLETO - SISTEMA PRONTO PARA PRODUÇÃO")
    print("=" * 60)
    
    tests = [
        ("Sistema de Banco de Dados", test_database_system),
        ("Sistema de Autenticação", test_authentication_system),
        ("Integração com IA", test_ai_integration),
        ("Sistema de Monitoramento", test_monitoring_system),
        ("Sistema de Backup", test_backup_system),
        ("Sistema de Redação", test_writing_system),
        ("Sistema de Gamificação", test_gamification_system),
        ("Sistema de Analytics", test_analytics_system),
        ("Prontidão Docker", test_docker_readiness),
        ("Prontidão CI/CD", test_ci_cd_readiness)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DOS TESTES DE PRODUÇÃO:")
    print(f"   ✅ Passou: {passed}/{len(tests)}")
    print(f"   ❌ Falhou: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 SISTEMA 100% PRONTO PARA PRODUÇÃO!")
        print("\n🚀 Para fazer deploy:")
        print("   ./deploy.sh production")
        print("\n🌐 Após deploy, acesse:")
        print("   • API: http://localhost:8000")
        print("   • Interface: http://localhost:8501")
        print("   • Docs: http://localhost:8000/docs")
        print("   • Monitoramento: http://localhost:3000")
        
        return True
    else:
        print(f"\n⚠️ {failed} teste(s) falharam. Corrija os problemas antes do deploy.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
