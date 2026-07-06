import unicodedata
from src.models import Author

class InvalidAuthorDataException(Exception):
    """Exceção levantada para dados inválidos de autor."""
    pass

class IdentityCurator:
    """Curador baseado em identidade do autor (Caso 4 e Caso 5)."""
    
    def __init__(self, authors: list[Author]):
        self.authors = authors

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

    def curate(self, unify_ids: bool = False) -> list[Author]:
        """Lógica comum para unificar nomes e IDs baseada em identidade."""
        if self.authors is None:
            raise InvalidAuthorDataException("Lista de autores não pode ser None.")

        groups = self._group_authors_by_identity()
        canonical_ids, canonical_names = self._define_canonical_authors(groups)

        result = []
        for author in self.authors:
            key = self._get_identity_key(author.nome)
            new_id = canonical_ids[key] if unify_ids else author.id
            result.append(Author(new_id, canonical_names[key]))

        return result

    def _group_authors_by_identity(self) -> dict[tuple, list[Author]]:
        """Agrupa autores que representam a mesma identidade."""
        groups = {}

        for author in self.authors:
            key = self._get_identity_key(author.nome)

            if key not in groups:
                groups[key] = []

            groups[key].append(author)

        return groups

    def _define_canonical_authors(
        self,
        groups: dict[tuple, list[Author]]
    ) -> tuple[dict[tuple, int], dict[tuple, str]]:
        """Define o ID e o nome canônico de cada grupo de autores."""
        canonical_ids = {}
        canonical_names = {}

        for key, group_authors in groups.items():
            canonical_ids[key] = min(a.id for a in group_authors)
            canonical_names[key] = self._select_best_author_name(group_authors)

        return canonical_ids, canonical_names

    def _select_best_author_name(self, authors: list[Author]) -> str:
        """Seleciona o nome com maior qualidade dentro de um grupo de autores."""
        best_name = authors[0].nome
        max_score = self._quality_score(best_name)

        for author in authors:
            score = self._quality_score(author.nome)

            if score > max_score:
                max_score = score
                best_name = author.nome

        return best_name

    def _get_identity_key(self, name: str) -> tuple:
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
            p_norm = self._normalize_name(p)
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
