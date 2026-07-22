from dataclasses import dataclass


@dataclass
class Achievement:
    id: int = 0
    title: str = ""
    completed: bool = False
