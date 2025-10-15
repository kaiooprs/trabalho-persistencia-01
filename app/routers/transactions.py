# app/routers/transactions.py

import hashlib
import io
import zipfile
from typing import List

from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import StreamingResponse

# Importa a instância do DB e os modelos/schemas
from app.db.delta_minidb import db
from app.models.transaction import TransactionCreate, TransactionOut

# Cria um router para agrupar os endpoints
router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# =================================================================
# F3: CRUD Completo (Create, Read, Update, Delete)
# =================================================================

# F1: Inserir uma nova transação (CREATE)
@router.post("/", response_model=TransactionOut, status_code=201)
def create_transaction(transaction: TransactionCreate):
    """
    Cria uma nova transação no banco de dados.
    """
    transaction_dict = transaction.model_dump()
    created_transaction = db.insert(transaction_dict)
    return created_transaction

# Ler uma transação específica (READ)
@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int):
    """
    Busca uma única transação pelo seu ID.
    """
    transaction = db.get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# Atualizar uma transação (UPDATE)
@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(transaction_id: int, transaction_update: TransactionCreate):
    """
    Atualiza uma transação existente.
    NOTA: O método PUT substitui o recurso inteiro.
    """
    update_data = transaction_update.model_dump()
    updated_transaction = db.update(transaction_id, update_data)
    
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction

# Deletar uma transação (DELETE)
@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int):
    """
    Deleta uma transação pelo seu ID.
    """
    if not db.get(transaction_id): # Verifica se existe antes de tentar deletar
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction_id)
    return Response(status_code=204) # Retorna 204 No Content, que não tem corpo

# =================================================================
# F2: Listar Transações com Paginação
# =================================================================
@router.get("/", response_model=List[TransactionOut])
def list_transactions(page: int = 1, size: int = 20):
    """
    Lista transações com paginação.
    Exemplo de uso: /transactions/?page=2&size=10
    """
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Page and size must be 1 or greater.")
        
    transactions = db.paginate(page=page, size=size)
    return transactions

# =================================================================
# F4: Contagem de Entidades
# =================================================================
@router.get("/utils/count", response_model=dict)
def count_transactions():
    """
    Retorna a quantidade total de transações no banco de dados.
    """
    total = db.count()
    return {"total_transactions": total}

# =================================================================
# F5: Download de Dados via Streaming (CSV em ZIP)
# =================================================================
@router.get("/utils/download_csv", response_class=StreamingResponse)
def download_transactions_as_csv_zip():
    """
    Faz o download de todas as transações em um arquivo CSV compactado (.zip).
    Os dados são processados via streaming para não sobrecarregar a memória.
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Usa um writer para escrever no arquivo dentro do zip
        with zip_file.open("transactions.csv", "w") as csv_buffer:
            # Converte o buffer de bytes para um writer de texto
            csv_writer = io.TextIOWrapper(csv_buffer, 'utf-8')
            
            # Escreve o cabeçalho do CSV
            header = [field.name for field in db.schema]
            csv_writer.write(",".join(header) + "\n")
            
            # Itera sobre os dados do DB em lotes para não usar memória
            scanner = db._scanner()
            for batch in scanner.to_batches():
                for row in batch.to_pylist():
                    csv_row = ",".join(map(str, row.values())) + "\n"
                    csv_writer.write(csv_row)
            
            csv_writer.flush() # Garante que tudo foi escrito no buffer

    zip_buffer.seek(0)
    
    headers = {'Content-Disposition': 'attachment; filename="transactions.zip"'}
    return StreamingResponse(zip_buffer, media_type="application/x-zip-compressed", headers=headers)

# =================================================================
# F6: Função de Hash
# =================================================================
@router.get("/utils/hash", response_model=dict)
def get_hash(data: str, algorithm: str = "sha256"):
    """
    Retorna o hash de um dado usando o algoritmo especificado (md5, sha1, sha256).
    Exemplo: /utils/hash?data=minhasenha&algorithm=sha1
    """
    supported_algorithms = ["md5", "sha1", "sha256"]
    if algorithm.lower() not in supported_algorithms:
        raise HTTPException(status_code=400, detail=f"Invalid algorithm. Use one of {supported_algorithms}.")

    hasher = getattr(hashlib, algorithm.lower())()
    hasher.update(data.encode('utf-8'))
    
    return {
        "original_data": data,
        "algorithm": algorithm.lower(),
        "hashed_value": hasher.hexdigest()
    }