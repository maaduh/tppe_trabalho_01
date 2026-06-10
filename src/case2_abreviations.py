import re
from src.models import Author

class Case2AbreviationsCurator:
    PARTICLES = {'de', 'do', 'da', 'dos', 'das', 'e'}

    @classmethod
    def curate(cls, authors: list[Author]) -> list[Author]:
        full_names_map = {}
        for author in authors:
            if not cls._is_abbreviation(author.nome):
                key = cls._get_full_name_match_key(author.nome)
                if key:
                    full_names_map[key] = author.nome

        curated_authors = []
        for author in authors:
            if cls._is_abbreviation(author.nome):
                abbrev_key = cls._get_abbreviation_match_key(author.nome)
                if abbrev_key in full_names_map:
                    curated_authors.append(Author(author.id, full_names_map[abbrev_key]))
                else:
                    curated_authors.append(Author(author.id, author.nome))
            else:
                curated_authors.append(Author(author.id, author.nome))
        
        return curated_authors

    @classmethod
    def _is_abbreviation(cls, name: str) -> bool:
        parts = cls._tokenize(name)
        if len(parts) < 2:
            return False
        
        full_words = [p for p in parts if len(p) > 1]
        return len(full_words) == 1

    @classmethod
    def _tokenize(cls, name: str) -> list[str]:
        clean_name = name.replace('.', ' ')
        return clean_name.split()

    @classmethod
    def _get_full_name_match_key(cls, name: str) -> tuple:
        parts = cls._tokenize(name)
        if not parts:
            return None
        
        surname = parts[-1].lower()
        initials = []
        for p in parts[:-1]:
            if p.lower() not in cls.PARTICLES:
                initials.append(p[0].upper())
        
        return (surname, tuple(initials))

    @classmethod
    def _get_abbreviation_match_key(cls, name: str) -> tuple:
        parts = cls._tokenize(name)
        if not parts:
            return None
        
        surname = ""
        initials = []
        for p in parts:
            if len(p) > 1:
                surname = p.lower()
            else:
                initials.append(p.upper())
        
        return (surname, tuple(initials))
