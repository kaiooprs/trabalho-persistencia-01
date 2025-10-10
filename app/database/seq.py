from pathlib import Path
from app.config import settings

# identificador atual da entidade
def _seq_path(entity: str) -> Path:
    root = Path(settings.DATA) / "seq"
    root.mkdir(parents=True, exist_ok=True)
    return root / f"{entity}.seq"

# autoincremento
def next_id(entity: str) -> int:
    p = _seq_path(entity)
    if not p.exists():
        p.write_text("0")
    current = int(p.read_text().strip() or "0")
    new = current + 1
    p.write_text(str(new))
    return new