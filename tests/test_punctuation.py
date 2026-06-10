import pytest

from src.data_curation import AuthorCurator


@pytest.mark.case1
def test_curation_punctuation(case1_punctuation_authors):

    result = AuthorCurator.curation_punctuation(
        case1_punctuation_authors
    )

    authors_by_id = {a.id: a.nome for a in result}

    # Veronica -> Verônica
    assert authors_by_id[31303] == "Verônica de Oliveira Moreira"
    assert authors_by_id[243352] == "Verônica de Oliveira Moreira"

    # Monica -> Mônica + apóstrofo correto
    assert authors_by_id[31299] == "Mônica Hirata Sant'anna"
    assert authors_by_id[433095] == "Mônica Hirata Sant'anna"

    # Goncalves -> Gonçalves
    assert authors_by_id[31298] == "Raphael Gonçalves Viana"
    assert authors_by_id[433094] == "Raphael Gonçalves Viana"

    # Lilian -> Lílian
    assert authors_by_id[899639] == "Lílian Luíza Viana Vieira"
    assert authors_by_id[243351] == "Lílian Luíza Viana Vieira"