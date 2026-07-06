from src.models import Author
from src.case2_abreviations import Case2AbreviationsCurator
from src.case3_conectives import Case3ConectivesCurator
from src.curation_punctuation import PunctuationCurator
from src.identity_curator import IdentityCurator, InvalidAuthorDataException

class AuthorCurator:

    @classmethod
    def curation_punctuation(cls, authors: list[Author]) -> list[Author]:
        return PunctuationCurator(authors).curate()

    @classmethod
    def curation_abreviations(cls, authors: list[Author]) -> list[Author]:
        """Caso 2: Sobrenome + Iniciais dos nomes.
        Deduplica unificando nomes completos e abreviados."""
        return Case2AbreviationsCurator.curate(authors)

    @classmethod
    def curation_conectives(cls, authors: list[Author]) -> list[Author]:
        """Caso 3: Partículas de e uso de ponto nas abreviações opcionais."""
        if authors is None:
            raise InvalidAuthorDataException("Lista de autores não pode ser None.")

        return Case3ConectivesCurator.curate(authors)

    @classmethod
    def curation_grouped_names(cls, authors: list[Author]) -> list[Author]:
        """Caso 4: Iniciais dos nomes agrupadas + sobrenome."""
        return IdentityCurator(authors).curate(unify_ids=False)

    @classmethod
    def curation_ids(cls, authors: list[Author]) -> list[Author]:
        """Caso 5: IDs diferentes para o mesmo autor."""
        return IdentityCurator(authors).curate(unify_ids=True)