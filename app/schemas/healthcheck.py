from typing import List

from pydantic import BaseModel


class Healthcheck(BaseModel):
    healthy: bool
    errors: List[str] = []
