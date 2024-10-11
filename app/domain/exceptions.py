from dataclasses import dataclass


@dataclass(eq=False)
class ValidationException(Exception):
    text: str

    @property
    def message(self) -> str:
        return "Base exception occurred"


@dataclass(eq=False)
class TextTooLongException(ValidationException):
    @property
    def message(self) -> str:
        return f"{self.text} is too long"


@dataclass(eq=False)
class ObsceneTextException(ValidationException):
    @property
    def message(self) -> str:
        return f"{self.text} is an obscene text"


@dataclass
class EmptyTextException(ValidationException):
    text: str = ""

    @property
    def message(self) -> str:
        return "Empty text"
