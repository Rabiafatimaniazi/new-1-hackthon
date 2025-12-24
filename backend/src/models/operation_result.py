"""
Operation result model
"""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class OperationResult:
    """
    Result of an operation
    """
    success: bool
    message: str
    error_code: Optional[str] = None
    data: Optional[Any] = None

    def to_dict(self) -> dict:
        """
        Convert the result to a dictionary

        Returns:
            dict: Result as dictionary
        """
        result = {
            "success": self.success,
            "message": self.message
        }
        if self.error_code:
            result["error_code"] = self.error_code
        if self.data:
            result["data"] = self.data
        return result