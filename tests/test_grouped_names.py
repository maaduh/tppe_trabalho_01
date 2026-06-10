import pytest
from src.models import Author
from src.data_curation import AuthorCurator

class TestGroupedNames:
    def test_curation_grouped_names_conftest(self, case4_grouped_names_authors):
        """Teste do Caso 4: Iniciais agrupadas + sobrenome usando dados do conftest."""
        result = AuthorCurator.curation_grouped_names(case4_grouped_names_authors)
        
        # Mapeamento do ID para o nome esperado após a deduplicação
        # Nota: Usamos nomes normalizados ou unificados conforme a lógica do AuthorCurator
        # No conftest: 31303 é "Veronica de Oliveira Moreira", 554799 é "Sergio Henrique Guaraldi"
        # 608303 (V. de O. Moreira) e 954057 (SH Guaraldi) devem ser unificados.
        
        expected_names = {
            31303: "Veronica de Oliveira Moreira",
            608303: "Veronica de Oliveira Moreira",
            554799: "Sergio Henrique Guaraldi",
            954057: "Sergio Henrique Guaraldi",
            31297: "Souza, L. O.", # Formato inverso que a lógica atual unifica para "L. O. Souza" ou similar se houver match
            549242: "Luiz de O. de Souza",
        }
        
        # Como o AuthorCurator unifica para a melhor grafia:
        # Para Souza: 31297 (Souza, L. O.) e 549242 (Luiz de O. de Souza)
        # 549242 é mais completo.
        
        for author in result:
            if author.id in [31303, 608303]:
                assert author.nome == "Veronica de Oliveira Moreira"
            elif author.id in [554799, 954057]:
                assert author.nome == "Sergio Henrique Guaraldi"
            elif author.id in [31297, 549242]:
                assert author.nome == "Luiz de O. de Souza"

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
