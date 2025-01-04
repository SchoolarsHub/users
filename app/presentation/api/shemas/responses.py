from dataclasses import dataclass, field


@dataclass(frozen=True)
class Response:
    status: int


@dataclass(frozen=True)
class SuccessResponse[ResultT](Response):
    result: ResultT | None = field(default=None)


@dataclass(frozen=True)
class ErrorData[ErrorT]:
    title: str = "Error occurred"
    data: ErrorT | None = field(default=None)


@dataclass(frozen=True)
class ErrorResponse[ErrorT](Response):
    error: ErrorData[ErrorT] = field(default_factory=ErrorData)
