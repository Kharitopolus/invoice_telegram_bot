from pydantic import BaseModel, ConfigDict


class ClientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    manager_id: int
    is_chat_with_manager_active: bool
