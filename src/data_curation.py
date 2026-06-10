import unicodedata
import re
from src.models import Author
from src.case2_abreviations import Case2AbreviationsCurator

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
        return Case2AbreviationsCurator.curate(authors)

    @classmethod
    def curation_conectives(cls, authors: list[Author]) -> list[Author]:
        """Caso 3: Partículas de e uso de ponto nas abreviações opcionais."""
        # ToDo
        pass

    @classmethod
    def curation_grouped_names(cls, authors: list[Author]) -> list[Author]:
        """Caso 4: Iniciais dos nomes agrupadas + sobrenome."""
        if authors is None:
            raise InvalidAuthorDataException(
                "Lista de autores não pode ser None."
            )

        # Partículas (preposições) que devem ser ignoradas na extração de iniciais
        PARTICLES = {'de', 'da', 'do', 'das', 'dos', 'e'}

        def extract_signature(name: str):
            """
            Extrai (sobrenome, tupla_de_iniciais) de um nome que NÃO contém vírgula.
            Pressupõe formato 'Nomes Sobrenome'.
            Exemplos:
                'Veronica de Oliveira Moreira' -> ('moreira', ('V', 'O'))
                'V. de O. Moreira'             -> ('moreira', ('V', 'O'))
                'SH Guaraldi'                  -> ('guaraldi', ('S', 'H'))
                'Sérgio Henrique Guaraldi'     -> ('guaraldi', ('S', 'H'))
            """
            name = ' '.join(name.split())  # normaliza espaços
            tokens = name.split()
            if not tokens:
                return '', ()

            surname = tokens[-1].lower()
            given_tokens = tokens[:-1]
            initials = []

            for token in given_tokens:
                clean = token.rstrip('.').lower()
                if clean in PARTICLES:
                    continue

                # Iniciais agrupadas (ex: "SH", "VC") -> cada letra vira uma inicial
                if token.isupper() and len(token) >= 2 and '.' not in token:
                    for ch in token:
                        initials.append(ch.upper())
                # Nome completo ou inicial com ponto (ex: "Veronica", "V.")
                else:
                    if clean:
                        initials.append(clean[0].upper())

            return surname, tuple(initials)

        # Separa autores com vírgula (formato invertido) – estes permanecem inalterados
        result = [None] * len(authors)
        non_comma_authors = []
        non_comma_indices = []

        for idx, author in enumerate(authors):
            if ',' in author.nome:
                result[idx] = author  # mantém o original
            else:
                non_comma_authors.append(author)
                non_comma_indices.append(idx)

        # Agrupa apenas os autores sem vírgula
        if non_comma_authors:
            groups = {}
            for idx, author in enumerate(non_comma_authors):
                sig = extract_signature(author.nome)
                groups.setdefault(sig, []).append((idx, author))

            # Escolhe o nome mais completo (mais longo) para cada grupo
            best_name_for_sig = {}
            for sig, members in groups.items():
                best_member = max(members, key=lambda m: len(m[1].nome))
                best_name_for_sig[sig] = best_member[1].nome

            # Aplica o nome canônico aos autores do grupo
            processed = []
            for author in non_comma_authors:
                sig = extract_signature(author.nome)
                canonical_name = best_name_for_sig[sig]
                processed.append(Author(author.id, canonical_name))

            # Insere os autores processados nas posições originais
            for pos, author in zip(non_comma_indices, processed):
                result[pos] = author
        else:
            # Se todos os autores têm vírgula, retorna a lista original
            return authors

        return result


    @classmethod
    def curation_ids(cls, authors: list[Author]) -> list[Author]:
        """Caso 5: IDs diferentes para o mesmo autor."""
        # ToDo
        pass
