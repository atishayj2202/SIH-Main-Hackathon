from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class CategoryInfo(DBSchemaBase):
    title: str
    category_id: UUID
    description: str
    article_info: str
    is_deleted: datetime | None = None
    remarks: str

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _CategoryInfo


_CategoryInfo = Base.from_schema_base(CategoryInfo, "category_info")
