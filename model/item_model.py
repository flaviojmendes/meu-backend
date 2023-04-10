from typing import Optional
from pydantic import BaseModel


class ItemModel(BaseModel):
    item_id: Optional[str]
    nickname: Optional[str]