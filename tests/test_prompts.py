"""
Testes automatizados para validação de prompts.

Garante que o prompt v2 atende aos requisitos mínimos do desafio:
estrutura, persona, formato, exemplos few-shot, ausência de TODOs
e técnicas declaradas nos metadados.

Como rodar:
    pytest tests/test_prompts.py -v
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path (mantido para compatibilidade com utils, se necessário)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def prompt_data():
    """Carrega o prompt v2 e retorna os dados internos (depois da chave raiz)."""
    raw = load_prompts(str(PROMPT_FILE))
    assert raw, f"Arquivo {PROMPT_FILE} está vazio ou inválido"
    root_key = list(raw.keys())[0]
    return raw[root_key]


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt_data, \
            "Campo 'system_prompt' não encontrado no YAML"

        system_prompt = prompt_data["system_prompt"]

        assert isinstance(system_prompt, str), \
            "Campo 'system_prompt' deve ser uma string"
        assert system_prompt.strip(), \
            "Campo 'system_prompt' está vazio"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = prompt_data.get("system_prompt", "")

        markers = [
            "Você é um", "Você é uma", "Você é o", "Você é a",
            "You are a", "You are an",
        ]
        has_role = any(marker in system_prompt for marker in markers)

        assert has_role, (
            f"O prompt não define uma persona explícita. "
            f"Esperado conter um dos marcadores: {markers}"
        )

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data.get("system_prompt", "").lower()

        format_markers = [
            "como um",                  # formato canônico ("Como um [persona]")
            "eu quero",                 # formato canônico ("eu quero [ação]")
            "para que",                 # formato canônico ("para que [benefício]")
            "user story",               # menção explícita
            "markdown",                 # formatação Markdown
            "critérios de aceitação",   # estrutura ágil
            "given-when-then",          # padrão Given-When-Then
            "dado que",                 # padrão Given em pt-BR
        ]
        has_format = any(marker in system_prompt for marker in format_markers)

        assert has_format, (
            f"O prompt não menciona formato esperado (User Story / Markdown / "
            f"Given-When-Then). Esperado um dos marcadores: {format_markers}"
        )

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data.get("system_prompt", "").lower()

        example_markers = [
            "## exemplos",
            "### exemplo",
            "exemplo 1",
            "exemplo:",
            "example 1",
        ]
        has_examples = any(marker in system_prompt for marker in example_markers)

        assert has_examples, (
            "O prompt não contém exemplos Few-shot. "
            "Esperado pelo menos um marcador: '## Exemplos', '### Exemplo' "
            "ou 'Exemplo 1'."
        )

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        forbidden_markers = ["[TODO]", "[todo]", "[Todo]"]

        for field, value in prompt_data.items():
            if isinstance(value, str):
                for marker in forbidden_markers:
                    assert marker not in value, (
                        f"Marcador '{marker}' encontrado no campo '{field}'. "
                        f"Resolva os TODOs antes de entregar."
                    )

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        tags = prompt_data.get("tags", [])

        assert isinstance(tags, list), \
            "Campo 'tags' deve ser uma lista no YAML"
        assert len(tags) >= 2, (
            f"Mínimo de 2 técnicas requeridas em 'tags', "
            f"encontradas: {len(tags)} ({tags})"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
