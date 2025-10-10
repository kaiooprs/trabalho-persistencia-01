from pydantic import BaseModel
import pyarrow as pa

account_schema = pa.schema([
    ("id", pa.int64()),
    ("name", pa.string()),
    # "Conta Corrente" , "Carteira" ou "Cartão"
    ("type", pa.string()),            
    ("initial_balance", pa.float64()),
    ("user_id", pa.int64()),
])

class AccountCreate(BaseModel):
    name: str
    type: str
    # saldo inicial
    initial_balance: float
    user_id: int

class AccountOut(AccountCreate):
    id: int