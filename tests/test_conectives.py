import pytest
from src.models import Author
from src.data_curation import AuthorCurator, InvalidAuthorDataException


@pytest.mark.case3
class TestConectives:
    def test_curation_conectives_conftest(self, case3_conectives_authors):
        """Teste do Caso 3: partículas e pontos opcionais usando dados do conftest."""
        result = AuthorCurator.curation_conectives(case3_conectives_authors)

        authors_by_id = {author.id: author.nome for author in result}

        assert authors_by_id[746937] == "Luiz de Oliveira de Souza"
        assert authors_by_id[608296] == "Luiz de Oliveira de Souza"
        assert authors_by_id[549242] == "Luiz de Oliveira de Souza"
        assert authors_by_id[28372] == "Ana de Mattos Seabra"
        assert authors_by_id[582585] == "Ana de Mattos Seabra"

    @pytest.mark.parametrize("input_list, expected_list", [
    (
        [
            Author(746937, "Luiz de Oliveira de Souza"),
            Author(608296, "Luiz Oliveira Souza"),
            Author(549242, "Luiz de O. de Souza"),
        ],
        [
            Author(746937, "Luiz de Oliveira de Souza"),
            Author(608296, "Luiz de Oliveira de Souza"),
            Author(549242, "Luiz de Oliveira de Souza"),
        ],
    ),
    (
        [
            Author(28372, "Ana de Mattos Seabra"),
            Author(582585, "Ana Mattos Seabra"),
            Author(582585, "Ana de M. Seabra"),
        ],
        [
            Author(28372, "Ana de Mattos Seabra"),
            Author(582585, "Ana de Mattos Seabra"),
            Author(582585, "Ana de Mattos Seabra"),
        ],
    ),
    (
        [
            Author(31303, "Verônica de Oliveira Moreira"),
            Author(608303, "Verônica Oliveira Moreira"),
            Author(608303, "Verônica de O. Moreira"),
        ],
        [
            Author(31303, "Verônica de Oliveira Moreira"),
            Author(608303, "Verônica de Oliveira Moreira"),
            Author(608303, "Verônica de Oliveira Moreira"),
        ],
    ),
])
    def test_curation_conectives_specific(self, input_list, expected_list):
        """Teste com mais de um conjunto de dados para o Caso 3."""
        result = AuthorCurator.curation_conectives(input_list)
        assert result == expected_list

    def test_curation_conectives_keeps_unrelated_authors_separated(self):
        """Autores com sobrenome e iniciais iguais, mas nomes completos diferentes, não devem ser agrupados."""
        input_list = [
            Author(1, "Luiz de Oliveira de Souza"),
            Author(2, "Luiz de Otavio de Souza"),
        ]

        result = AuthorCurator.curation_conectives(input_list)

        assert result == input_list

    @pytest.mark.exceptions
    def test_curation_conectives_none_raises_exception(self):
        """Fluxo de exceção: a lista de autores não pode ser None."""
        with pytest.raises(InvalidAuthorDataException):
            AuthorCurator.curation_conectives(None)
