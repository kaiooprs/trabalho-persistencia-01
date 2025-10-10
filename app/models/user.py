from pydantic import BaseModel, EmailStr
from datetime import datetime
import pyarrow as pa

# PyArrow schema para Delta Lake

user_schema = pa.schema([
    ("id", pa.int64()),
    ("name", pa.string()),
    ("email", pa.string()),
    ("password_hash", pa.string()),
    # ISO
    ("created_at", pa.string()),  
])

# entrada de dados - quando usuario cria uma conta via POST
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# resposta da API - evita vazamento de hash
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: str

# armazenamento no Delta Lake - usado para consultas
class UserDB(BaseModel):
    id: int 
    name: str
    email: EmailStr
    password_hash: str
    created_at: str
