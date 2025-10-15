# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI

# Importe a instância db e o router
from app.db.delta_minidb import db
from app.routers import transactions

# Crie o gerenciador de "lifespan"
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado ANTES do servidor iniciar
    print("Initializing application...")
    db.create_table_if_not_exists()
    yield
    # Código a ser executado APÓS o servidor desligar (se necessário)
    print("Shutting down application...")

# Cria a aplicação FastAPI e conecta o lifespan
app = FastAPI(
    title="💰 Finance API",
    description="API para controle de despesas pessoais usando FastAPI e Delta Lake.",
    version="1.0.0",
    lifespan=lifespan  # <<--- ADICIONE ESTA LINHA
)

# Mensagem de boas-vindas na rota raiz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API Financeira! Acesse /docs para ver a documentação."}

# Inclui o router de transações
app.include_router(transactions.router)