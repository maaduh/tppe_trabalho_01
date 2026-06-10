import pytest
from src.models import Author
from src.data_curation import AuthorCurator

class TestAbreviations:
    
    @pytest.mark.parametrize("input_list, expected_list", [
        (
            [
                Author(28372, "Ana de Mattos Seabra"), 
                Author(582585, "Seabra A M")
            ],
            [
                Author(28372, "Ana de Mattos Seabra"), 
                Author(582585, "Ana de Mattos Seabra")
            ]
        ),
        (
            [
                Author(28371, "Cassius de Souza"), 
                Author(746936, "Souza C.")
            ],
            [
                Author(28371, "Cassius de Souza"), 
                Author(746936, "Cassius de Souza")
            ]
        ),
        (
            [
                Author(1, "Pedro Henrique Silva"),
                Author(2, "Silva P. H.")
            ],
            [
                Author(1, "Pedro Henrique Silva"),
                Author(2, "Pedro Henrique Silva")
            ]
        ),
        (
            [
                Author(28372, "Ana de Mattos Seabra"), 
                Author(582585, "A. M. Seabra")
            ],
            [
                Author(28372, "Ana de Mattos Seabra"), 
                Author(582585, "Ana de Mattos Seabra")
            ]
        ),
        (
            [
                Author(10, "Maria das Dores Santos"),
                Author(11, "Silva J."),
                Author(12, "Santos M D"),
                Author(13, "João da Silva")
            ],
            [
                Author(10, "Maria das Dores Santos"),
                Author(11, "João da Silva"),
                Author(12, "Maria das Dores Santos"),
                Author(13, "João da Silva")
            ]
        )
    ])
    def test_curation_abreviations(self, input_list, expected_list):
        result = AuthorCurator.curation_abreviations(input_list)
        assert result == expected_list

    def test_curation_abreviations_no_match(self):
        input_list = [
            Author(123, "João Silva"), 
            Author(456, "Santos M.")
        ]
        result = AuthorCurator.curation_abreviations(input_list)
        assert result == input_list
