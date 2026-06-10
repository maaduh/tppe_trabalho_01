import pytest
from src.models import Author
from src.data_curation import AuthorCurator

class TestGroupedNames:
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
    def test_curation_grouped_names(self, input_list, expected_list):
        result = AuthorCurator.curation_grouped_names(input_list)
        assert result == expected_list

    def test_curation_grouped_names_no_match(self):
        input_list = [Author(123, "Nome Um Silva"), Author(456, "Outro Nome")]
        result = AuthorCurator.curation_grouped_names(input_list)
        assert result == input_list
