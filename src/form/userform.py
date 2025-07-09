from typing import Optional

from pydantic import BaseModel, Field


class UserForm(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=2,
        max_length=64,
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=32,
    )
    desc: Optional[str] = Field(
        None,
        min_length=1,
        max_length=256,
    )
