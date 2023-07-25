from typing import NamedTuple, Optional, Any

class CodeBlob(NamedTuple):
    code: str = ""
    stdout: Optional[str] = ""
    error: Optional[str] = ""
    tb: Optional[str] = ""
    buggy: Optional[bool] = False
    execution_killed: bool = False
    execution_time: float = 0.0
    environment: Optional[Any] = None # Not sure about this one