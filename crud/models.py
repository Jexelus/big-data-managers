from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Manager(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    contracts_count: int = 0