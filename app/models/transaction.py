from pydantic import BaseModel
import pyarrow as pa

transaction_schema = pa.schema([
    ("id", pa.int64()),
    ("description", pa.string()),
    ("amount", pa.float64()),
     # ISO YYYY-MM-DD
    ("date", pa.string()),      
    ("type", pa.string()),      
    ("account_id", pa.int64()),
    ("category_id", pa.int64()),
    ("user_id", pa.int64()),
])

class TransactionCreate(BaseModel):
    description: str
    amount: float
    date: str
    type: str
    account_id: int
    category_id: int
    user_id: int

class TransactionOut(TransactionCreate):
    id: int
