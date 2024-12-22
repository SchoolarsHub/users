from dataclasses import dataclass, field


@dataclass(frozen=True)
class Response:
    status: int


@dataclass(frozen=True)
class SuccessfulResponse[ResultT](Response):
    result: ResultT | None = None


@dataclass(frozen=True)
class Data[ErrorT]:
    message: str = "Error occurred"
    data: ErrorT | None = None


@dataclass(frozen=True)
class ErrorResponse[ErrorT](Response):
    error: Data[ErrorT] = field(default_factory=Data)
