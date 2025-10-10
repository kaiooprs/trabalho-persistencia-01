from pydantic import BaseModel
import pyarrow as pa

category_schema = pa.schema([
    ("id", pa.int64()),
    ("name", pa.string()),
    ("kind", pa.string()),    
    ("user_id", pa.int64()),
])

class CategoryCreate(BaseModel):
    name: str
    kind: str
    user_id: int

class CategoryOut(CategoryCreate):
    id: int
