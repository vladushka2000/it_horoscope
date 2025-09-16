from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ConfigMixin:
    model_config = ConfigDict(populate_by_name=True)
