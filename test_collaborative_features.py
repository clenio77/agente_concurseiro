#!/usr/bin/env python3
"""
Teste dos Recursos Colaborativos - Fase 2
Valida funcionalidades de grupos, mentoria e compartilhamento
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_collaborative_component():
    """Testa o componente de recursos colaborativos"""
    print("🧪 TESTANDO COLLABORATIVE FEATURES COMPONENT")
    print("="*60)
    
    try:
        from app.components.collaborative_features import CollaborativeFeatures, GroupType, MemberRole, MessageType
        
        # Criar instância
        cf = CollaborativeFeatures()
        print("✅ CollaborativeFeatures instanciado com sucesso")
        
        # Testar inicialização de dados
        assert hasattr(cf, 'initialize_session_state')
        print("✅ Método de inicialização presente")
        
        # Testar geração de grupos de exemplo
        sample_groups = cf.generate_sample_groups()
        assert len(sample_groups) > 0
        print(f"✅ Grupos de exemplo gerados: {len(sample_groups)} grupos")
        
        # Verificar estrutura dos grupos
        sample_group = sample_groups[0]
        required_fields = [
            'id', 'name', 'description', 'type', 'members_count', 'max_members',
            'created_date', 'last_activity', 'admin', 'tags', 'activity_level',
            'success_rate', 'avg_study_hours', 'is_member'
        ]
        
        for field in required_fields:
            assert field in sample_group, f"Campo {field} não encontrado"
        
        print("✅ Estrutura dos grupos válida")
        
        # Testar enums
        assert isinstance(sample_group['type'], GroupType)
        print("✅ Enum GroupType funcionando")
        
        # Testar geração de dados de mentoria
        mentorship_data = cf.generate_mentorship_data()
        assert len(mentorship_data) > 0
        print(f"✅ Dados de mentoria gerados: {len(mentorship_data)} mentores")
        
        # Verificar estrutura de mentoria
        mentor = mentorship_data[0]
        mentor_fields = [
            'id', 'mentor_name', 'mentor_expertise', 'mentor_rating',
            'mentor_experience', 'status', 'sessions_completed', 'match_score',
            'specialties', 'availability'
        ]
        
        for field in mentor_fields:
            assert field in mentor, f"Campo {field} não encontrado em mentor"
        
        print("✅ Estrutura de mentoria válida")
        
        # Testar geração de materiais
        materials = cf.generate_sample_materials()
        assert len(materials) > 0
        print(f"✅ Materiais gerados: {len(materials)} materiais")
        
        # Verificar estrutura de materiais
        material = materials[0]
        material_fields = [
            'id', 'title', 'type', 'subject', 'author', 'upload_date',
            'downloads', 'rating', 'size', 'description', 'tags',
            'verified', 'premium', 'comments_count'
        ]
        
        for field in material_fields:
            assert field in material, f"Campo {field} não encontrado em material"
        
        print("✅ Estrutura de materiais válida")
        
        # Testar geração de mensagens
        messages = cf.generate_sample_messages()
        assert isinstance(messages, dict)
        assert len(messages) > 0
        print(f"✅ Mensagens geradas para {len(messages)} grupos")
        
        # Verificar estrutura de mensagens
        first_group_messages = list(messages.values())[0]
        if first_group_messages:
            message = first_group_messages[0]
            message_fields = ['id', 'author', 'content', 'timestamp', 'type', 'reactions', 'replies']
            
            for field in message_fields:
                assert field in message, f"Campo {field} não encontrado em mensagem"
            
            assert isinstance(message['type'], MessageType)
            print("✅ Estrutura de mensagens válida")
        
        # Testar estatísticas de colaboração
        stats = cf.generate_collaboration_stats()
        assert isinstance(stats, dict)
        assert 'weekly_activity' in stats
        assert 'engagement_by_day' in stats
        assert 'popular_subjects' in stats
        assert 'mentorship_success' in stats
        print("✅ Estatísticas de colaboração geradas")
        
        print("🎉 COLLABORATIVE FEATURES COMPONENT: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de Recursos Colaborativos: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_group_management():
    """Testa funcionalidades de gerenciamento de grupos"""
    print("\n🧪 TESTANDO GERENCIAMENTO DE GRUPOS")
    print("="*60)
    
    try:
        from app.components.collaborative_features import CollaborativeFeatures, GroupType
        
        cf = CollaborativeFeatures()
        
        # Testar filtros de grupos
        groups = cf.generate_sample_groups()
        
        # Testar filtro por busca
        filtered = cf.filter_groups(groups, "Direito", "Todos", "Atividade Recente")
        assert isinstance(filtered, list)
        print("✅ Filtro por busca funcionando")
        
        # Testar filtro por tipo
        filtered = cf.filter_groups(groups, "", "Público", "Mais Membros")
        public_groups = [g for g in filtered if g['type'] == GroupType.PUBLICO]
        assert len(public_groups) == len(filtered) or len(filtered) == 0
        print("✅ Filtro por tipo funcionando")
        
        # Testar ordenação
        filtered = cf.filter_groups(groups, "", "Todos", "Taxa de Sucesso")
        if len(filtered) > 1:
            # Verificar se está ordenado por taxa de sucesso (decrescente)
            rates = [g['success_rate'] for g in filtered]
            is_sorted = all(rates[i] >= rates[i+1] for i in range(len(rates)-1))
            assert is_sorted, "Grupos não estão ordenados por taxa de sucesso"
            print("✅ Ordenação por taxa de sucesso funcionando")
        
        # Testar obtenção de grupos do usuário
        user_groups = cf.get_user_groups()
        assert isinstance(user_groups, list)
        print(f"✅ Grupos do usuário obtidos: {len(user_groups)} grupos")
        
        # Verificar se grupos do usuário têm campos adicionais
        if user_groups:
            user_group = user_groups[0]
            user_fields = ['user_role', 'join_date', 'contributions', 'last_seen']
            
            for field in user_fields:
                assert field in user_group, f"Campo {field} não encontrado em grupo do usuário"
            
            print("✅ Estrutura de grupos do usuário válida")
        
        print("🎉 GERENCIAMENTO DE GRUPOS: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de gerenciamento: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_mentorship_system():
    """Testa sistema de mentoria"""
    print("\n🧪 TESTANDO SISTEMA DE MENTORIA")
    print("="*60)
    
    try:
        from app.components.collaborative_features import CollaborativeFeatures
        
        cf = CollaborativeFeatures()
        
        # Testar dados de mentoria
        mentorships = cf.generate_mentorship_data()
        
        # Verificar distribuição de status
        statuses = [m['status'] for m in mentorships]
        unique_statuses = set(statuses)
        expected_statuses = {'ativo', 'disponível', 'pausado'}
        
        assert unique_statuses.issubset(expected_statuses), f"Status inválidos encontrados: {unique_statuses - expected_statuses}"
        print("✅ Status de mentoria válidos")
        
        # Verificar ratings
        ratings = [m['mentor_rating'] for m in mentorships]
        assert all(1.0 <= rating <= 5.0 for rating in ratings), "Ratings fora do intervalo válido"
        print("✅ Ratings de mentores válidos")
        
        # Verificar match scores
        match_scores = [m['match_score'] for m in mentorships]
        assert all(0.0 <= score <= 1.0 for score in match_scores), "Match scores fora do intervalo válido"
        print("✅ Match scores válidos")
        
        # Testar especialidades
        for mentor in mentorships:
            assert isinstance(mentor['specialties'], list), "Especialidades devem ser uma lista"
            assert len(mentor['specialties']) > 0, "Mentor deve ter pelo menos uma especialidade"
        
        print("✅ Especialidades de mentores válidas")
        
        # Testar disponibilidade
        availabilities = [m['availability'] for m in mentorships]
        expected_availabilities = {"Manhã", "Tarde", "Noite", "Fins de semana", "Flexível"}
        
        for availability in availabilities:
            assert availability in expected_availabilities, f"Disponibilidade inválida: {availability}"
        
        print("✅ Disponibilidades válidas")
        
        print("🎉 SISTEMA DE MENTORIA: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de mentoria: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_material_sharing():
    """Testa sistema de compartilhamento de materiais"""
    print("\n🧪 TESTANDO COMPARTILHAMENTO DE MATERIAIS")
    print("="*60)
    
    try:
        from app.components.collaborative_features import CollaborativeFeatures
        
        cf = CollaborativeFeatures()
        
        # Testar geração de materiais
        materials = cf.generate_sample_materials()
        
        # Verificar tipos de materiais
        types = [m['type'] for m in materials]
        expected_types = {"PDF", "Vídeo", "Áudio", "Planilha", "Mapa Mental", "Resumo"}
        unique_types = set(types)
        
        assert unique_types.issubset(expected_types), f"Tipos inválidos: {unique_types - expected_types}"
        print("✅ Tipos de materiais válidos")
        
        # Verificar ratings
        ratings = [m['rating'] for m in materials]
        assert all(0.0 <= rating <= 5.0 for rating in ratings), "Ratings fora do intervalo válido"
        print("✅ Ratings de materiais válidos")
        
        # Verificar downloads
        downloads = [m['downloads'] for m in materials]
        assert all(download >= 0 for download in downloads), "Downloads não podem ser negativos"
        print("✅ Contadores de download válidos")
        
        # Testar filtros de materiais
        filtered = cf.filter_materials(materials, "Direito", "Todos", "Todas", "Mais Recentes")
        assert isinstance(filtered, list)
        print("✅ Filtro de materiais funcionando")
        
        # Testar filtro por tipo
        filtered = cf.filter_materials(materials, "", "PDF", "Todas", "Mais Baixados")
        pdf_materials = [m for m in filtered if m['type'] == 'PDF']
        assert len(pdf_materials) == len(filtered) or len(filtered) == 0
        print("✅ Filtro por tipo de material funcionando")
        
        # Testar ordenação por downloads
        filtered = cf.filter_materials(materials, "", "Todos", "Todas", "Mais Baixados")
        if len(filtered) > 1:
            downloads = [m['downloads'] for m in filtered]
            is_sorted = all(downloads[i] >= downloads[i+1] for i in range(len(downloads)-1))
            assert is_sorted, "Materiais não estão ordenados por downloads"
            print("✅ Ordenação por downloads funcionando")
        
        # Verificar tags
        for material in materials:
            assert isinstance(material['tags'], list), "Tags devem ser uma lista"
        
        print("✅ Tags de materiais válidas")
        
        # Verificar flags booleanas
        for material in materials:
            assert isinstance(material['verified'], bool), "Campo 'verified' deve ser booleano"
            assert isinstance(material['premium'], bool), "Campo 'premium' deve ser booleano"
        
        print("✅ Flags booleanas válidas")
        
        print("🎉 COMPARTILHAMENTO DE MATERIAIS: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de materiais: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_communication_system():
    """Testa sistema de comunicação"""
    print("\n🧪 TESTANDO SISTEMA DE COMUNICAÇÃO")
    print("="*60)
    
    try:
        from app.components.collaborative_features import CollaborativeFeatures, MessageType
        
        cf = CollaborativeFeatures()
        
        # Testar geração de mensagens
        messages = cf.generate_sample_messages()
        
        # Verificar estrutura das mensagens
        for group_id, group_messages in messages.items():
            assert isinstance(group_messages, list), "Mensagens do grupo devem ser uma lista"
            
            for message in group_messages:
                # Verificar campos obrigatórios
                required_fields = ['id', 'author', 'content', 'timestamp', 'type']
                for field in required_fields:
                    assert field in message, f"Campo {field} não encontrado na mensagem"
                
                # Verificar tipos
                assert isinstance(message['type'], MessageType), "Tipo de mensagem inválido"
                assert isinstance(message['timestamp'], datetime), "Timestamp deve ser datetime"
                assert isinstance(message['reactions'], int), "Reactions deve ser int"
                assert isinstance(message['replies'], int), "Replies deve ser int"
        
        print("✅ Estrutura de mensagens válida")
        
        # Testar ordenação de mensagens por timestamp
        for group_messages in messages.values():
            if len(group_messages) > 1:
                timestamps = [m['timestamp'] for m in group_messages]
                is_sorted = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
                assert is_sorted, "Mensagens não estão ordenadas por timestamp"
        
        print("✅ Ordenação de mensagens funcionando")
        
        # Testar geração de conteúdo de mensagem
        sample_content = cf.generate_sample_message_content()
        assert isinstance(sample_content, str), "Conteúdo da mensagem deve ser string"
        assert len(sample_content) > 0, "Conteúdo da mensagem não pode estar vazio"
        print("✅ Geração de conteúdo de mensagem funcionando")
        
        # Testar tipos de mensagem
        message_types = set()
        for group_messages in messages.values():
            for message in group_messages:
                message_types.add(message['type'])
        
        # Verificar se há diversidade de tipos
        assert len(message_types) > 1, "Deve haver diversidade nos tipos de mensagem"
        print("✅ Diversidade de tipos de mensagem")
        
        print("🎉 SISTEMA DE COMUNICAÇÃO: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de comunicação: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_collaborative_tests():
    """Executa todos os testes de recursos colaborativos"""
    print("🚀 INICIANDO TESTES DE RECURSOS COLABORATIVOS - FASE 2")
    print("="*80)
    
    results = []
    
    # Executar testes
    results.append(("Collaborative Features Component", test_collaborative_component()))
    results.append(("Gerenciamento de Grupos", test_group_management()))
    results.append(("Sistema de Mentoria", test_mentorship_system()))
    results.append(("Compartilhamento de Materiais", test_material_sharing()))
    results.append(("Sistema de Comunicação", test_communication_system()))
    
    # Resumo dos resultados
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES - RECURSOS COLABORATIVOS")
    print("="*80)
    
    passed = 0
    total = len(results)
    
    for component, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{component:35} | {status}")
        if result:
            passed += 1
    
    print("-"*80)
    print(f"TOTAL: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES DE RECURSOS COLABORATIVOS PASSARAM!")
        print("✅ Sistema de grupos de estudo funcionando")
        print("✅ Sistema de mentoria operacional")
        print("✅ Compartilhamento de materiais ativo")
        print("✅ Sistema de comunicação integrado")
        print("✅ Analytics colaborativos implementados")
        return True
    else:
        print(f"\n⚠️ {total-passed} TESTES FALHARAM!")
        print("❌ Correções necessárias antes do deploy")
        return False

if __name__ == "__main__":
    success = run_collaborative_tests()
    
    if success:
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Integrar recursos colaborativos ao sistema principal")
        print("2. Implementar persistência de dados em tempo real")
        print("3. Adicionar notificações push para grupos")
        print("4. Desenvolver app mobile companion")
        print("5. Implementar recursos de moderação avançados")
    else:
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrigir testes que falharam")
        print("2. Validar integrações entre componentes")
        print("3. Testar com dados reais de usuários")
        print("4. Executar testes novamente")
        
    sys.exit(0 if success else 1)
