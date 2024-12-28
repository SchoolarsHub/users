from dataclasses import dataclass, field


@dataclass(eq=False)
class DomainError(Exception):
    title: str = field(default="Domain Error occured")
