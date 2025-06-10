from fastapi import APIRouter

from app.api.routes import auth, flashcards, performance, quizzes, study_plans, users

api_router = APIRouter()

# Incluir rotas de autenticação
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Incluir rotas de usuários
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Incluir rotas de planos de estudo
api_router.include_router(study_plans.router, prefix="/study-plans", tags=["study-plans"])

# Incluir rotas de quizzes
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])

# Incluir rotas de flashcards
api_router.include_router(flashcards.router, prefix="/flashcards", tags=["flashcards"])

# Incluir rotas de desempenho
api_router.include_router(performance.router, prefix="/performance", tags=["performance"])
