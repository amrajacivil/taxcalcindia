from typing import Optional, Dict, Any

class TaxCalculationException(Exception):
    """Base exception for the taxcalcindia package.

    Attributes:
        message: Human readable error message.
        code: Optional machine-readable error code.
        details: Optional additional context (e.g. input values).
    """
    def __init__(self, message: str = "Tax calculation error",
                 *, code: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable representation of the error."""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "details": self.details,
        }

    def __str__(self) -> str:
        base = f"{self.__class__.__name__}: {self.message}"
        if self.code:
            base += f" (code={self.code})"
        return base

class InputValidationError(TaxCalculationException):
    """Raised when input validation fails."""
    pass

class CalculationError(TaxCalculationException):
    """Raised when a calculation step fails."""
    pass

class DataNotFoundError(TaxCalculationException):
    """Raised when required data (rates, slabs, etc.) is missing."""
    pass

__all__ = [
    "TaxCalculationException",
    "InputValidationError",
    "CalculationError",
    "DataNotFoundError",
]
