# Trabalho Prático 1 - TDD

Trabalho prático de Test-Driven Development (TDD) para curadoria de dados de repositórios científicos.

## Integrantes do Grupo
- Felipe Nunes de Mello - 202023627
- João Victor Felix Moreira - 231037709
- Maria Eduarda Araujo Pereira - 231026474
- Pedro Túlio Curvelo Camilo - 231011785
- Víctor Moreira Almeida - 221008481

## Tecnologias Utilizadas
- **Linguagem:** Python 3.12 
- **Framework de Testes:** pytest 8.4.2

## Instruções de Execução dos Testes

Para executar os testes, certifique-se de ter o `pytest` instalado e execute o seguinte comando na raiz do repositório:

```bash
pytest tests/nome_do_arquivo_de_teste_aqui
```
exemplos:

```bash
pytest tests/test_abreviations.py
```
```bash
pytest tests/test_conectives.py
```
```bash
pytest tests/test_grouped_names.py
```
```bash
pytest tests/test_ids.py
```
```bash
pytest tests/test_punctuation.py
```

## Metodologia TDD (Caso 2)
O desenvolvimento do Caso 2 seguiu a metodologia **Red-Green-Refactor**:

1.  **Red:** Criação de testes unitários no `tests/test_abreviations.py` com base nos exemplos do enunciado e casos de borda (como iniciais vindo antes do sobrenome).
2.  **Green:** Implementação da lógica mínima necessária em `src/case2_abreviations.py` para fazer os testes passarem.
3.  **Refactor:** Melhoria do código para suportar flexibilidade na ordem das iniciais (ex: "Silva J." e "J. Silva") e inclusão de (*de, do, da, e, etc.*) na lógica de comparação.
