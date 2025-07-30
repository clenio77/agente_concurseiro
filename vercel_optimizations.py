"""
Otimizações específicas para Vercel
- Gerenciamento de memória
- Timeout handling
- Cache otimizado
- Processamento em chunks
"""

import os
import gc
import time
import functools
from typing import Any, Callable, Optional
import streamlit as st

class VercelOptimizer:
    """Otimizações para funcionar dentro dos limites do Vercel"""
    
    # Limites do Vercel
    MAX_EXECUTION_TIME = 60  # segundos (Hobby plan)
    MAX_MEMORY_MB = 1024     # MB
    MAX_FILE_SIZE_MB = 10    # MB para upload
    
    def __init__(self):
        self.start_time = time.time()
        self.memory_threshold = self.MAX_MEMORY_MB * 0.8  # 80% do limite
    
    def check_timeout(self, operation_name: str = "operação") -> bool:
        """Verifica se está próximo do timeout"""
        elapsed = time.time() - self.start_time
        remaining = self.MAX_EXECUTION_TIME - elapsed
        
        if remaining < 10:  # Menos de 10 segundos restantes
            st.warning(f"⏰ Timeout próximo! Restam {remaining:.1f}s para {operation_name}")
            return True
        
        return False
    
    def optimize_memory(self):
        """Força limpeza de memória"""
        gc.collect()
        
        # Limpar cache do Streamlit se necessário
        if hasattr(st, 'cache_data'):
            try:
                st.cache_data.clear()
            except:
                pass
    
    def validate_file_size(self, file_size_bytes: int) -> bool:
        """Valida tamanho do arquivo"""
        size_mb = file_size_bytes / (1024 * 1024)
        
        if size_mb > self.MAX_FILE_SIZE_MB:
            st.error(f"❌ Arquivo muito grande! Máximo: {self.MAX_FILE_SIZE_MB}MB, "
                    f"Atual: {size_mb:.1f}MB")
            return False
        
        return True
    
    def process_in_chunks(self, data: str, chunk_size: int = 1000) -> list:
        """Processa texto em chunks para evitar timeout"""
        chunks = []
        
        for i in range(0, len(data), chunk_size):
            if self.check_timeout("processamento em chunks"):
                st.warning("⏰ Processamento interrompido por timeout")
                break
            
            chunk = data[i:i + chunk_size]
            chunks.append(chunk)
            
            # Limpeza de memória a cada 10 chunks
            if len(chunks) % 10 == 0:
                self.optimize_memory()
        
        return chunks
    
    def timeout_decorator(self, timeout_seconds: int = 30):
        """Decorator para funções com timeout"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    # Executar função
                    result = func(*args, **kwargs)
                    
                    # Verificar se demorou muito
                    elapsed = time.time() - start_time
                    if elapsed > timeout_seconds:
                        st.warning(f"⏰ Função {func.__name__} demorou {elapsed:.1f}s "
                                 f"(limite: {timeout_seconds}s)")
                    
                    return result
                
                except Exception as e:
                    elapsed = time.time() - start_time
                    st.error(f"❌ Erro em {func.__name__} após {elapsed:.1f}s: {str(e)}")
                    raise
            
            return wrapper
        return decorator
    
    @staticmethod
    def cache_with_ttl(ttl_seconds: int = 300):
        """Cache com TTL para Vercel"""
        def decorator(func: Callable) -> Callable:
            @st.cache_data(ttl=ttl_seconds, show_spinner=False)
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Instância global
vercel_optimizer = VercelOptimizer()

# Decorators de conveniência
def with_timeout(timeout_seconds: int = 30):
    """Decorator para timeout"""
    return vercel_optimizer.timeout_decorator(timeout_seconds)

def with_cache(ttl_seconds: int = 300):
    """Decorator para cache"""
    return VercelOptimizer.cache_with_ttl(ttl_seconds)

# Funções de conveniência
def check_timeout(operation: str = "operação") -> bool:
    """Verifica timeout"""
    return vercel_optimizer.check_timeout(operation)

def optimize_memory():
    """Otimiza memória"""
    vercel_optimizer.optimize_memory()

def validate_file_size(file_size: int) -> bool:
    """Valida tamanho do arquivo"""
    return vercel_optimizer.validate_file_size(file_size)

def process_in_chunks(data: str, chunk_size: int = 1000) -> list:
    """Processa em chunks"""
    return vercel_optimizer.process_in_chunks(data, chunk_size)

# Classe para monitoramento de performance
class PerformanceMonitor:
    """Monitor de performance para Vercel"""
    
    def __init__(self):
        self.metrics = {
            'start_time': time.time(),
            'operations': [],
            'memory_usage': [],
            'warnings': []
        }
    
    def start_operation(self, name: str):
        """Inicia monitoramento de operação"""
        operation = {
            'name': name,
            'start_time': time.time(),
            'end_time': None,
            'duration': None,
            'success': None
        }
        self.metrics['operations'].append(operation)
        return len(self.metrics['operations']) - 1  # Retorna índice
    
    def end_operation(self, operation_index: int, success: bool = True):
        """Finaliza monitoramento de operação"""
        if operation_index < len(self.metrics['operations']):
            operation = self.metrics['operations'][operation_index]
            operation['end_time'] = time.time()
            operation['duration'] = operation['end_time'] - operation['start_time']
            operation['success'] = success
            
            # Adicionar warning se demorou muito
            if operation['duration'] > 10:  # Mais de 10 segundos
                warning = f"⚠️ Operação '{operation['name']}' demorou {operation['duration']:.1f}s"
                self.metrics['warnings'].append(warning)
                st.warning(warning)
    
    def get_summary(self) -> dict:
        """Retorna resumo de performance"""
        total_time = time.time() - self.metrics['start_time']
        successful_ops = sum(1 for op in self.metrics['operations'] if op.get('success', False))
        total_ops = len(self.metrics['operations'])
        
        return {
            'total_execution_time': total_time,
            'total_operations': total_ops,
            'successful_operations': successful_ops,
            'success_rate': (successful_ops / total_ops * 100) if total_ops > 0 else 0,
            'warnings_count': len(self.metrics['warnings']),
            'average_operation_time': sum(
                op.get('duration', 0) for op in self.metrics['operations']
            ) / total_ops if total_ops > 0 else 0
        }
    
    def display_metrics(self):
        """Exibe métricas no Streamlit"""
        summary = self.get_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⏱️ Tempo Total", f"{summary['total_execution_time']:.1f}s")
        
        with col2:
            st.metric("🔄 Operações", f"{summary['successful_operations']}/{summary['total_operations']}")
        
        with col3:
            st.metric("✅ Taxa de Sucesso", f"{summary['success_rate']:.1f}%")
        
        with col4:
            st.metric("⚠️ Warnings", summary['warnings_count'])
        
        # Mostrar warnings se houver
        if self.metrics['warnings']:
            with st.expander("⚠️ Warnings de Performance"):
                for warning in self.metrics['warnings']:
                    st.warning(warning)

# Monitor global
performance_monitor = PerformanceMonitor()

# Context manager para operações
class OperationContext:
    """Context manager para monitorar operações"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.operation_index = None
    
    def __enter__(self):
        self.operation_index = performance_monitor.start_operation(self.operation_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        success = exc_type is None
        performance_monitor.end_operation(self.operation_index, success)
        
        if not success:
            st.error(f"❌ Erro na operação '{self.operation_name}': {exc_val}")

# Função de conveniência para context manager
def monitor_operation(operation_name: str):
    """Context manager para monitorar operação"""
    return OperationContext(operation_name)
