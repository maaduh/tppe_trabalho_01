import pytest
from src.models import Author
from src.data_curation import AuthorCurator

class TestConectives:
    def test_curation_conectives_conftest(self, case3_conectives_authors):
        """Teste do Caso 3: Partículas e pontos opcionais usando dados do conftest."""
        result = AuthorCurator.curation_conectives(case3_conectives_authors)
        
        # Luiz de Oliveira de Souza (IDs: 746937, 608296, 549242)
        # Deve unificar para o nome mais completo
        expected_name = "Luiz de Oliveira de Souza"
        
        for author in result:
            if author.id in [746937, 608296, 549242]:
                assert author.nome == expected_name

    @pytest.mark.parametrize("input_list, expected_list", [
        (
            [
                Author(746937, "Luiz de Oliveira de Souza"), 
                Author(608296, "Luiz Oliveira Souza"),
                Author(549242, "Luiz de O. de Souza")
            ],
            [
                Author(746937, "Luiz de Oliveira de Souza"), 
                Author(608296, "Luiz de Oliveira de Souza"),
                Author(549242, "Luiz de Oliveira de Souza")
            ]
        )
    ])
    def test_curation_conectives_specific(self, input_list, expected_list):
        """Teste com os exemplos específicos do enunciado."""
        result = AuthorCurator.curation_conectives(input_list)
        assert result == expected_list
