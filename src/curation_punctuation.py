import unicodedata
import re
from src.models import Author

class InvalidAuthorDataException(Exception):
    """Exceção levantada para dados inválidos de autor."""
    pass

class PunctuationCurator:
    """Objeto-método para o Caso 1: unificação de diferenças tipográficas."""
    
    def __init__(self, authors: list[Author]):
        self.authors = authors
        self.canonical_names = {}
    
    def curate(self) -> list[Author]:
        if self.authors is None:
            raise InvalidAuthorDataException("Lista de autores não pode ser None.")
        
        self._build_canonical_map()
        return self._apply_canonical_names()
    
    def _build_canonical_map(self):
        for author in self.authors:
            key = self._normalize_name(author.nome)
            if (key not in self.canonical_names or
                self._quality_score(author.nome) > self._quality_score(self.canonical_names[key])):
                self.canonical_names[key] = author.nome.replace("’", "'").replace("`", "'")
    
    def _apply_canonical_names(self) -> list[Author]:
        result = []
        for author in self.authors:
            key = self._normalize_name(author.nome)
            result.append(Author(author.id, self.canonical_names[key]))
        return result
    

    @staticmethod
    def _normalize_name(nome: str) -> str:
        """Gera uma chave de comparação ignorando acentos e tipos de apóstrofo."""
        nome = nome.replace("’", "'").replace("`", "'")

        nome = unicodedata.normalize("NFD", nome)
        nome = "".join(
            c for c in nome
            if unicodedata.category(c) != "Mn"
        )

        return nome.lower().strip()

    @staticmethod
    def _quality_score(nome: str) -> int:
        """
        Quanto maior a pontuação, mais 'correto' o nome é considerado.
        Dá preferência para caracteres acentuados e nomes mais longos.
        """
        score = 0

        for c in nome:
            decomposed = unicodedata.normalize("NFD", c)
            if any(unicodedata.category(x) == "Mn" for x in decomposed):
                score += 10

        score += nome.count("'") * 3
        
        # Preferência por nomes mais longos (geralmente menos abreviados)
        score += len(nome)

        return score