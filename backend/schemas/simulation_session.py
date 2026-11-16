from typing import Literal, Optional

from pydantic import BaseModel


class SimulationSessionFinish(BaseModel):
    status: Literal["completed", "stopped", "failed"]
    error_message: Optional[str] = None
