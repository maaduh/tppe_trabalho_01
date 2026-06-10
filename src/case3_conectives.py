import re
import unicodedata
from dataclasses import dataclass

from src.models import Author


@dataclass(frozen=True)
class _NameTerm:
    value: str
    is_initial: bool


@dataclass(frozen=True)
class _NameSignature:
    surname: str
    terms: tuple[_NameTerm, ...]


class Case3ConectivesCurator:
    """
    Caso 3: considera equivalentes nomes que variam apenas pela omissao
    de particulas (de, da, do, etc.) e pelo uso opcional de ponto em
    abreviacoes.

    Exemplo:
    - Luiz de Oliveira de Souza
    - Luiz Oliveira Souza
    - Luiz de O. de Souza

    Todos possuem a mesma assinatura: sobrenome Souza + termos L/O.
    A forma canonica escolhida e a mais completa dentre os registros do grupo.
    """

    PARTICLES = {"de", "da", "do", "das", "dos", "e"}

    @classmethod
    def curate(cls, authors: list[Author]) -> list[Author]:
        groups: list[dict] = []

        for author in authors:
            signature = cls._signature(author.nome)
            group = cls._find_compatible_group(groups, signature)

            if group is None:
                groups.append({"signature": signature, "authors": [author]})
            else:
                group["signature"] = cls._merge_signatures(
                    group["signature"],
                    signature,
                )
                group["authors"].append(author)

        canonical_by_author_key: dict[tuple[int, str], str] = {}
        for group in groups:
            canonical_name = cls._choose_canonical_name(group["authors"])
            for author in group["authors"]:
                canonical_by_author_key[(author.id, author.nome)] = canonical_name

        return [
            Author(author.id, canonical_by_author_key[(author.id, author.nome)])
            for author in authors
        ]

    @classmethod
    def _find_compatible_group(cls, groups: list[dict], signature: _NameSignature):
        for group in groups:
            if cls._are_compatible(group["signature"], signature):
                return group
        return None

    @classmethod
    def _are_compatible(cls, left: _NameSignature, right: _NameSignature) -> bool:
        if left.surname != right.surname:
            return False

        if len(left.terms) != len(right.terms):
            return False

        return all(
            cls._terms_are_compatible(left_term, right_term)
            for left_term, right_term in zip(left.terms, right.terms)
        )

    @staticmethod
    def _terms_are_compatible(left: _NameTerm, right: _NameTerm) -> bool:
        if not left.value or not right.value:
            return False

        if not left.is_initial and not right.is_initial:
            return left.value == right.value

        return left.value[0] == right.value[0]

    @classmethod
    def _merge_signatures(
        cls,
        left: _NameSignature,
        right: _NameSignature,
    ) -> _NameSignature:
        merged_terms = []

        for left_term, right_term in zip(left.terms, right.terms):
            if left_term.is_initial and not right_term.is_initial:
                merged_terms.append(right_term)
            else:
                merged_terms.append(left_term)

        return _NameSignature(left.surname, tuple(merged_terms))

    @classmethod
    def _signature(cls, name: str) -> _NameSignature:
        tokens = cls._tokens(name)
        semantic_tokens = [
            token for token in tokens
            if cls._normalize(token) not in cls.PARTICLES
        ]

        if not semantic_tokens:
            return _NameSignature("", tuple())

        surname = cls._normalize(semantic_tokens[-1])
        terms = tuple(
            _NameTerm(
                value=cls._normalize(token),
                is_initial=len(cls._normalize(token)) == 1,
            )
            for token in semantic_tokens[:-1]
        )

        return _NameSignature(surname=surname, terms=terms)

    @classmethod
    def _tokens(cls, name: str) -> list[str]:
        reordered_name = cls._reorder_comma_name(name)
        cleaned_name = reordered_name.replace("’", "'").replace("`", "'")
        return re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ']+", cleaned_name)

    @staticmethod
    def _reorder_comma_name(name: str) -> str:
        if "," not in name:
            return name

        parts = [part.strip() for part in name.split(",", maxsplit=1)]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return name

        return f"{parts[1]} {parts[0]}"

    @staticmethod
    def _normalize(value: str) -> str:
        normalized = unicodedata.normalize("NFD", value)
        without_accents = "".join(
            char for char in normalized
            if unicodedata.category(char) != "Mn"
        )
        return without_accents.lower().strip()

    @classmethod
    def _choose_canonical_name(cls, authors: list[Author]) -> str:
        return max(authors, key=lambda author: cls._quality_score(author.nome)).nome

    @classmethod
    def _quality_score(cls, name: str) -> tuple[int, int, int, int]:
        tokens = cls._tokens(name)
        normalized_tokens = [cls._normalize(token) for token in tokens]

        particles_count = sum(
            1 for token in normalized_tokens
            if token in cls.PARTICLES
        )
        full_terms_count = sum(
            1 for token in normalized_tokens
            if token not in cls.PARTICLES and len(token) > 1
        )
        accent_count = sum(
            1 for char in name
            if any(
                unicodedata.category(decomposed) == "Mn"
                for decomposed in unicodedata.normalize("NFD", char)
            )
        )

        return (
            full_terms_count,
            particles_count,
            accent_count,
            len(name),
        )
