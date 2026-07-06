import unicodedata
import re
from src.models import Author
from src.case2_abreviations import Case2AbreviationsCurator
from src.case3_conectives import Case3ConectivesCurator

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
        return cls._curate_by_identity(authors, unify_ids=False)

    @classmethod
    def _curate_by_identity(cls, authors: list[Author], unify_ids: bool = False) -> list[Author]:
        """Lógica comum para unificar nomes e IDs baseada em identidade."""
        if authors is None:
            raise InvalidAuthorDataException("Lista de autores não pode ser None.")

        groups = cls._group_authors_by_identity(authors)
        canonical_ids, canonical_names = cls._define_canonical_authors(groups)

        result = []
        for author in authors:
            key = cls._get_identity_key(author.nome)
            new_id = canonical_ids[key] if unify_ids else author.id
            result.append(Author(new_id, canonical_names[key]))

        return result

    @classmethod
    def _group_authors_by_identity(cls, authors: list[Author]) -> dict[tuple, list[Author]]:
        """Agrupa autores que representam a mesma identidade."""
        groups = {}

        for author in authors:
            key = cls._get_identity_key(author.nome)

            if key not in groups:
                groups[key] = []

            groups[key].append(author)

        return groups

    @classmethod
    def _define_canonical_authors(
        cls,
        groups: dict[tuple, list[Author]]
    ) -> tuple[dict[tuple, int], dict[tuple, str]]:
        """Define o ID e o nome canônico de cada grupo de autores."""
        canonical_ids = {}
        canonical_names = {}

        for key, group_authors in groups.items():
            canonical_ids[key] = min(a.id for a in group_authors)
            canonical_names[key] = cls._select_best_author_name(group_authors)

        return canonical_ids, canonical_names

    @classmethod
    def _select_best_author_name(cls, authors: list[Author]) -> str:
        """Seleciona o nome com maior qualidade dentro de um grupo de autores."""
        best_name = authors[0].nome
        max_score = cls._quality_score(best_name)

        for author in authors:
            score = cls._quality_score(author.nome)

            if score > max_score:
                max_score = score
                best_name = author.nome

        return best_name

    @classmethod
    def _get_identity_key(cls, name: str) -> tuple:
        """Gera uma chave de identidade para agrupar diferentes grafias do mesmo autor."""
        # 1. Trata inversão por vírgula
        if ',' in name:
            parts = [x.strip() for x in name.split(',')]
            if len(parts) == 2:
                name = f"{parts[1]} {parts[0]}"
        
        # 2. Tokeniza e remove pontos
        name = name.replace('.', ' ')
        parts = name.split()
        if not parts:
            return ("", ())
            
        particles = {'de', 'do', 'da', 'dos', 'das', 'e'}
        
        surname = ""
        initials = []
        
        # 3. Identifica sobrenome e iniciais
        for p in parts:
            p_norm = cls._normalize_name(p)
            if p_norm in particles:
                continue
                
            if len(p) > 1:
                # Caso 4: Iniciais agrupadas (ex: SH, AM, VC)
                vowels = set('aeiou')
                has_vowels = any(c.lower() in vowels for c in p)
                
                # Heurística para iniciais agrupadas
                if p.isupper() and (not has_vowels or len(p) <= 2):
                    for char in p:
                        initials.append(char.upper())
                else:
                    if surname:
                        initials.append(surname[0].upper())
                    surname = p_norm
            else:
                initials.append(p.upper())
                
        return (surname, tuple(sorted(initials)))

    @classmethod
    def curation_ids(cls, authors: list[Author]) -> list[Author]:
        """Caso 5: IDs diferentes para o mesmo autor."""
        return cls._curate_by_identity(authors, unify_ids=True)