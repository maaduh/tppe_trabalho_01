"""
Fixtures compartilhadas entre todas as suites de teste.
Organizadas por casos de teste.
"""
import sys
import os
from pathlib import Path

import pytest


# Adiciona o diretório pai ao path para importar os módulos do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
root_dir = Path(__file__).parent.parent.resolve()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.models import Author # classe Author (id, nome)
from src.data_curation import AuthorCurator


# ======================================================================
# Fixtures organizadas por caso de teste (AuthorCurator)
# ======================================================================

@pytest.fixture
def case1_punctuation_authors() -> list[Author]:
    """
    CASO 1: Diferenças de grafia (acentos, pontuação, apóstrofos, maiúsculas).
    """
    return [
        Author(31303,  "Veronica de Oliveira Moreira"),
        Author(243352, "Verônica de Oliveira Moreira"),
        Author(31299,  "Monica Hirata Sant`anna"),
        Author(433095, "Mônica Hirata Sant’anna"),
        Author(31298,  "Raphael Goncalves Viana"),
        Author(433094, "Raphael Gonçalves Viana"),
        Author(899639, "Lilian Luíza Viana Vieira"),
        Author(243351, "Lílian Luíza Viana Vieira"),
    ]


@pytest.fixture
def case2_abbreviations_authors() -> list[Author]:
    """
    CASO 2: Sobrenome + Iniciais dos nomes (com ou sem pontos).
    """
    return [
        Author(28371,  "Cassius de Souza"),
        Author(746936, "Souza C."),
        Author(746936, "C. Souza"),
        Author(608303, "Moreira V O"),
        Author(608303, "Moreira V. de O."),
        Author(549244, "Sant'anna M. H."),
        Author(608298, "M. H. Sant'anna"),
    ]


@pytest.fixture
def case3_conectives_authors() -> list[Author]:
    """
    CASO 3: Partículas (de, da, do, de Oliveira etc.) e uso opcional de ponto.
    """
    return [
        Author(746937, "Luiz de Oliveira de Souza"),
        Author(608296, "Luiz Oliveira Souza"),
        Author(549242, "Luiz de O. de Souza"),
        Author(28372,  "Ana de Mattos Seabra"),
        Author(582585, "Ana Mattos Seabra"),
        Author(243350, "Sérgio Henrique Guaraldi"),
        Author(954057, "Sérgio Henrique Guaraldi"),
    ]


@pytest.fixture
def case4_grouped_names_authors() -> list[Author]:
    """
    CASO 4: Iniciais dos nomes agrupadas + sobrenome (ex: "V. de O. Moreira", "SH Guaraldi").
    """
    return [
        Author(31303,  "Veronica de Oliveira Moreira"),
        Author(608303, "V. de O. Moreira"),
        Author(554799, "Sergio Henrique Guaraldi"),
        Author(954057, "SH Guaraldi"),
        Author(31297,  "Souza, L. O."),
        Author(549242, "Luiz de O. de Souza"),
    ]


@pytest.fixture
def case5_ids_authors() -> list[Author]:
    """
    CASO 5: IDs diferentes para o mesmo autor.
    """
    return [
        # Raphael Gonçalves Viana – 5 IDs diferentes
        Author(31298,  "Raphael Goncalves Viana"),
        Author(433094, "Raphael Gonçalves Viana"),
        Author(549243, "Raphael Gonçalves Viana"),
        Author(608297, "Raphael Gonçalves Viana"),
        Author(746938, "Raphael Gonçalves Viana"),
        # Ana de Mattos Seabra – 2 IDs diferentes
        Author(28372,  "Ana de Mattos Seabra"),
        Author(243349, "Ana de Mattos Seabra"),
        # Sérgio Henrique Guaraldi – IDs diferentes
        Author(554799, "Sergio Henrique Guaraldi"),
        Author(243350, "Sérgio Henrique Guaraldi"),
        Author(954057, "SH Guaraldi"),
        # Vanilda Cristina Junior – IDs diferentes
        Author(763027, "Vanilda Cristina Junior"),
        Author(335284, "Vanilda Cristina Júnior"),
    ]


# ======================================================================
# Fixtures auxiliares (agrupamentos por autor real)
# ======================================================================

@pytest.fixture
def authors_ana() -> list[Author]:
    """Todos os registros da autora Ana de Mattos Seabra."""
    return [
        Author(28372,  "Ana de Mattos Seabra"),
        Author(243349, "Ana de Mattos Seabra"),
        Author(582585, "A. M. Seabra"),
        Author(582585, "Seabra A. M."),
        Author(582585, "AM Seabra"),
        Author(582585, "Ana Mattos Seabra"),
    ]


@pytest.fixture
def authors_raphael() -> list[Author]:
    """Todos os registros do autor Raphael Gonçalves Viana."""
    return [
        Author(31298,  "Raphael Goncalves Viana"),
        Author(433094, "Raphael Gonçalves Viana"),
        Author(549243, "Raphael Gonçalves Viana"),
        Author(608297, "Raphael Gonçalves Viana"),
        Author(746938, "Raphael Gonçalves Viana"),
    ]


@pytest.fixture
def all_authors(authors_ana, authors_raphael) -> list[Author]:
    """Lista com registros de múltiplos autores distintos (integração)."""
    outros = [
        Author(28371,  "Cassius de Souza"),
        Author(746936, "Cassius Souza"),
        Author(31303,  "Veronica de Oliveira Moreira"),
        Author(243352, "Verônica de Oliveira Moreira"),
        Author(746937, "Luiz de Oliveira de Souza"),
        Author(608296, "Luiz Oliveira Souza"),
        Author(31299,  "Monica Hirata Sant`anna"),
        Author(433095, "Mônica Hirata Sant’anna"),
        Author(763027, "Vanilda Cristina Junior"),
        Author(335284, "Vanilda Cristina Júnior"),
        Author(554799, "Sergio Henrique Guaraldi"),
        Author(243350, "Sérgio Henrique Guaraldi"),
        Author(899639, "Lilian Luíza Viana Vieira"),
        Author(243351, "Lílian Luíza Viana Vieira"),
        Author(713897, "Yuri Vieira Faria"),
    ]
    return authors_ana + authors_raphael + outros