from dataclasses import dataclass, field


@dataclass(eq=False)
class ApplicationError(Exception):
    title: str = field(default="Application Error occured")
