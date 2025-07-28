from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import auth, flashcards, performance, quizzes, study_plans, users
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

API_PREFIX = settings.API_PREFIX
app.include_router(auth.router, prefix=API_PREFIX, tags=["Auth"])
app.include_router(users.router, prefix=f"{API_PREFIX}/users", tags=["Users"])
app.include_router(study_plans.router, prefix=f"{API_PREFIX}/study-plans", tags=["Study Plans"])
app.include_router(quizzes.router, prefix=f"{API_PREFIX}/quizzes", tags=["Quizzes"])
app.include_router(flashcards.router, prefix=f"{API_PREFIX}/flashcards", tags=["Flashcards"])
app.include_router(performance.router, prefix=f"{API_PREFIX}/performance", tags=["Performance"])

@app.get("/")
def read_root():
    return {"message": f"Bem-vindo à API do {settings.PROJECT_NAME}"}
