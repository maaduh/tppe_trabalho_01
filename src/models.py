from dataclasses import dataclass

@dataclass
class Author:
    id: int
    nome: str

    def __eq__(self, other):
        if not isinstance(other, Author):
            return False
        return self.id == other.id and self.nome == other.nome
