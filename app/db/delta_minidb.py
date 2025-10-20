from __future__ import annotations
from typing import Any, Dict, Iterable, List, Optional
from pathlib import Path

import pyarrow as pa
import pyarrow.dataset as ds
from deltalake import DeltaTable, write_deltalake

from app.config import settings
from app.db.seq import next_id
from app.models.transaction import transaction_schema

class DeltaMiniDB:
    """

    Mini-DB sobre Delta Lake com CRUD, paginação, count e vacuum.
    Não carrega a tabela inteira em RAM.
    
    """
    def __init__(self, entity: str, schema: pa.schema, partition_by: Optional[List[str]] = None):
        self.entity = entity
        self.schema = schema
        self.partition_by = partition_by or []
        self.table_path = Path(settings.DATA) / "delta" / entity
        self.table_path.mkdir(parents=True, exist_ok=True)
        #self._ensure_table()

    def create_table_if_not_exists(self):
        """
        Cria a estrutura da tabela Delta (metadados) se ela não existir.
        Usa DeltaTable.create() que é o método ideal para inicialização.
        """
        if not (self.table_path / "_delta_log").exists():
            try:
                DeltaTable.create(
                    table_uri=str(self.table_path),
                    schema=self.schema,
                    partition_by=self.partition_by,
                )
                print(f"Delta table created successfully at: {self.table_path}")
            except Exception as e:
                print(f"Failed to create Delta table: {e}")
                raise e
    
    def _dt(self) -> DeltaTable:
        return DeltaTable(str(self.table_path))

    # ---------- Helpers ----------
    def _scanner(self, columns: Optional[List[str]] = None, filter_expr: Optional[Any] = None) -> ds.Scanner:
        dataset = self._dt().to_pyarrow_dataset()
        return ds.Scanner.from_dataset(dataset, columns=columns, filter=filter_expr)

    # ---------- CRUD ----------
    def insert(self, record: Dict[str, Any]) -> Dict[str, Any]:
        # autoincrement id (se não vier)
        if "id" not in record or record["id"] is None:
            record["id"] = next_id(self.entity)
        table = pa.Table.from_pylist([record], schema=self.schema)
        write_deltalake(str(self.table_path), table, mode="append", partition_by=self.partition_by)
        return record

    def get(self, _id: int) -> Optional[Dict[str, Any]]:
        sc = self._scanner(filter_expr=(ds.field("id") == _id))
        for batch in sc.to_batches():
            for row in batch.to_pylist():
                return row
        return None

    def update(self, _id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        current = self.get(_id)
        if not current:
            return None
        # delete e re-insere (merge simples e eficiente)
        self.delete(_id)
        current.update(updates)
        current["id"] = _id
        return self.insert(current)

    def delete(self, _id: int) -> bool:
        # Delta Lake possui delete eficiente
        self._dt().delete(f"id = {_id}")
        return True

    # ---------- Paginação e contagem ----------
    def paginate(self, page: int, size: int, filter_expr: Optional[Any] = None) -> List[Dict[str, Any]]:
        assert page >= 1 and size >= 1
        sc = self._scanner(filter_expr=filter_expr)
        start = (page - 1) * size
        out: List[Dict[str, Any]] = []
        seen = 0
        for batch in sc.to_batches():
            rows = batch.to_pylist()
            for r in rows:
                if seen >= start and len(out) < size:
                    out.append(r)
                seen += 1
                if len(out) == size:
                    return out
        return out

    def count(self, filter_expr: Optional[Any] = None) -> int:
        sc = self._scanner(filter_expr=filter_expr)
        total = 0
        for batch in sc.to_batches():
            total += batch.num_rows
        return total

    # ---------- Vacuum ----------
    def vacuum(self, retention_hours: int = 0) -> Dict[str, Any]:
        # remove arquivos ; retention_hours=0 (marcados pelo delete)
        deleted = self._dt().vacuum(retention_hours=retention_hours, dry_run=False)
        return {"deleted_files": deleted}



db = DeltaMiniDB(entity="transactions", schema=transaction_schema)