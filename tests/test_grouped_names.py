import pytest
from src.models import Author
from src.data_curation import AuthorCurator
class TestGroupedNames:
    def test_curation_grouped_names_conftest(self, case4_grouped_names_authors):
        """Teste do Caso 4: Iniciais agrupadas + sobrenome usando dados do conftest."""
        result = AuthorCurator.curation_grouped_names(case4_grouped_names_authors)
        
        # Mapeamento do ID para o nome esperado após a deduplicação
        expected_names = {
            31303: "Veronica de Oliveira Moreira",
            608303: "Veronica de Oliveira Moreira",  # v. de o. moreira -> full
            554799: "Sergio Henrique Guaraldi",
            954057: "Sergio Henrique Guaraldi",      # sh guaraldi -> full
            31297: "Souza, L. O.",                   # Não se aplica (formato inverso)
            549242: "Luiz de O. de Souza",           # Não se aplica
        }
        
        for author in result:
            assert author.nome == expected_names[author.id]
    @pytest.mark.parametrize("input_list, expected_list", [
        (
            [Author(763027, "Vanilda Cristina Junior"), Author(763027, "VC Junior")],
            [Author(763027, "Vanilda Cristina Junior"), Author(763027, "Vanilda Cristina Junior")]
        ),
        (
            [Author(243350, "Sérgio Henrique Guaraldi"), Author(954057, "SH Guaraldi")],
            [Author(243350, "Sérgio Henrique Guaraldi"), Author(954057, "Sérgio Henrique Guaraldi")]
        ),
        (
            [Author(31303, "Veronica de Oliveira Moreira"), Author(608303, "V. de O. Moreira")],
            [Author(31303, "Veronica de Oliveira Moreira"), Author(608303, "Veronica de Oliveira Moreira")]
        )
    ])
    
    def test_curation_grouped_names_specific(self, input_list, expected_list):
        """Teste com os exemplos específicos do enunciado."""
        result = AuthorCurator.curation_grouped_names(input_list)
        assert result == expected_list
    def test_curation_grouped_names_no_match(self):
        """Garante que autores sem relação não sejam agrupados."""
        input_list = [Author(123, "Nome Um Silva"), Author(456, "Outro Nome")]
        result = AuthorCurator.curation_grouped_names(input_list)
        assert result == input_list
