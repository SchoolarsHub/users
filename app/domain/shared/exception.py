from dataclasses import dataclass, field


@dataclass(eq=False)
class DomainError(Exception):
    message: str = field(default="Domain Error occured")
