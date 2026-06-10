import pytest
from src.models import Author
from src.data_curation import AuthorCurator

@pytest.mark.case5
def test_curation_ids(case5_ids_authors):
    """
    Teste do Caso 5: IDs diferentes para o mesmo autor.
    O ID de menor valor deve ser eleito para todos os registros do mesmo autor.
    """
    result = AuthorCurator.curation_ids(case5_ids_authors)
    
    # Criar um mapeamento de ID original para o ID curado para facilitar a verificação
    curated_authors_by_original_index = {i: author for i, author in enumerate(result)}

    # Raphael Gonçalves Viana (IDs: 31298, 433094, 549243, 608297, 746938)
    # Menor ID: 31298
    for i in range(0, 5):
        assert result[i].id == 31298

    # Ana de Mattos Seabra (IDs: 28372, 243349)
    # Menor ID: 28372
    assert result[5].id == 28372
    assert result[6].id == 28372

    # Sérgio Henrique Guaraldi (IDs: 554799, 243350, 954057)
    # Menor ID: 243350
    assert result[7].id == 243350
    assert result[8].id == 243350
    assert result[9].id == 243350

    # Vanilda Cristina Junior (IDs: 763027, 335284)
    # Menor ID: 335284
    assert result[10].id == 335284
    assert result[11].id == 335284

def test_curation_ids_none():
    """Teste para garantir que levanta exceção se a lista for None."""
    from src.data_curation import InvalidAuthorDataException
    with pytest.raises(InvalidAuthorDataException):
        AuthorCurator.curation_ids(None)

def test_curation_ids_multiple_unrelated():
    """Teste com autores não relacionados para garantir que IDs não são alterados indevidamente."""
    authors = [
        Author(1, "Joao Silva"),
        Author(2, "Maria Santos"),
        Author(3, "Silva, J."),
    ]
    result = AuthorCurator.curation_ids(authors)
    
    # Joao Silva and Silva, J. should be unified
    # Maria Santos stays same
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[2].id == 1
    
    assert result[0].nome == "Joao Silva"
    assert result[2].nome == "Joao Silva"
