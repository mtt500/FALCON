from pydantic import BaseModel
from typing import List, Optional

class Function(BaseModel):
    name: str
    address: str
    size: int
    calls: List[str]
    complexity: float
    importance_score: Optional[float] = None
    decompiled_code: Optional[str] = None