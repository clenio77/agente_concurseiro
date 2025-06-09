class BaseAppException(Exception):
    """
    Exceção base para a aplicação.
    """
    def __init__(self, message: str = "Erro na aplicação"):
        self.message = message
        super().__init__(self.message)

class AuthenticationError(BaseAppException):
    """
    Exceção para erros de autenticação.
    """
    def __init__(self, message: str = "Erro de autenticação"):
        super().__init__(message)

class DatabaseError(BaseAppException):
    """
    Exceção para erros de banco de dados.
    """
    def __init__(self, message: str = "Erro no banco de dados"):
        super().__init__(message)

class ValidationError(BaseAppException):
    """
    Exceção para erros de validação.
    """
    def __init__(self, message: str = "Erro de validação"):
        super().__init__(message)

class ResourceNotFoundError(BaseAppException):
    """
    Exceção para recursos não encontrados.
    """
    def __init__(self, resource: str = "Recurso"):
        super().__init__(f"{resource} não encontrado")

class PermissionError(BaseAppException):
    """
    Exceção para erros de permissão.
    """
    def __init__(self, message: str = "Permissão insuficiente"):
        super().__init__(message)
