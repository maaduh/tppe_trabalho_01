import unicodedata
import re
from src.models import Author
from src.case2_abreviations import Case2AbreviationsCurator

class InvalidAuthorDataException(Exception):
    """Exceção levantada para dados inválidos de autor."""
    pass

class AuthorCurator:
    
    @classmethod
    def curation_punctuation(cls, authors: list[Author]) -> list[Author]:
        """Caso 1: Diferenças de grafia (tipográficas).
        Unifica registros baseados no mesmo nome ignorando acentos/pontuação, 
        priorizando a versão com a acentuação e pontuação corretas."""
        # ToDo
        pass

    @classmethod
    def curation_abreviations(cls, authors: list[Author]) -> list[Author]:
        """Caso 2: Sobrenome + Iniciais dos nomes.
        Deduplica unificando nomes completos e abreviados."""
        return Case2AbreviationsCurator.curate(authors)

    @classmethod
    def curation_conectives(cls, authors: list[Author]) -> list[Author]:
        """Caso 3: Partículas de e uso de ponto nas abreviações opcionais."""
        # ToDo
        pass

    @classmethod
    def curation_grouped_names(cls, authors: list[Author]) -> list[Author]:
        """Caso 4: Iniciais dos nomes agrupadas + sobrenome."""
        # ToDo
        pass

    @classmethod
    def curation_ids(cls, authors: list[Author]) -> list[Author]:
        """Caso 5: IDs diferentes para o mesmo autor."""
        # ToDo
        pass
