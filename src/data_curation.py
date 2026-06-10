import unicodedata
import re
from src.models import Author

class InvalidAuthorDataException(Exception):
    """Exceção levantada para dados inválidos de autor."""
    pass

class AuthorCurator:
    

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
        Dá preferência para caracteres acentuados.
        """
        score = 0

        for c in nome:
            decomposed = unicodedata.normalize("NFD", c)
            if any(unicodedata.category(x) == "Mn" for x in decomposed):
                score += 10

        score += nome.count("'") * 3

        return score



    @classmethod
    def curation_punctuation(cls, authors: list[Author]) -> list[Author]:
        """Caso 1: Diferenças de grafia (tipográficas).
        Unifica registros baseados no mesmo nome ignorando acentos/pontuação, 
        priorizando a versão com a acentuação e pontuação corretas."""

        if authors is None:
            raise InvalidAuthorDataException(
                "Lista de autores não pode ser None."
            )

        canonical_names = {}

        # Descobre a melhor grafia para cada autor
        for author in authors:
            key = cls._normalize_name(author.nome)

            if (
                key not in canonical_names
                or cls._quality_score(author.nome)
                > cls._quality_score(canonical_names[key])
            ):
                canonical_names[key] = (
                    author.nome
                    .replace("’", "'")
                    .replace("`", "'")
                )

        # Atualiza todos os registros
        result = []
        for author in authors:
            key = cls._normalize_name(author.nome)

            result.append(
                Author(
                    author.id,
                    canonical_names[key]
                )
            )

        return result

    @classmethod
    def curation_abreviations(cls, authors: list[Author]) -> list[Author]:
        """Caso 2: Sobrenome + Iniciais dos nomes.
        Deduplica unificando nomes completos e abreviados."""
        # ToDo
        pass

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
