"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
import json
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    try:
        print(f"\n📤 Enviando prompt: {prompt_name}")

        client = Client()

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"])
        ])

        client.push_prompt(
            prompt_name,
            object=chat_prompt,
            is_public=True,
            description=prompt_data.get("description", ""),
            tags=prompt_data.get("tags", [])
        )

        print("✅ Push realizado com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    errors = []

    required_fields = ["system_prompt", "user_prompt"]

    for field in required_fields:
        if field not in prompt_data or not prompt_data[field].strip():
            errors.append(f"Campo obrigatório ausente ou vazio: {field}")

    return (len(errors) == 0, errors)


def main():
    print_section_header("PUSH DE PROMPTS PARA LANGSMITH")

    check_env_vars([
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT",
        "USERNAME_LANGSMITH_HUB"
    ])

    # Carrega o YAML
    data = load_yaml("prompts/bug_to_user_story_v2.yml")

    # O YAML tem uma chave raiz
    prompt_key = list(data.keys())[0]
    prompt_data = data[prompt_key]

    # Validação
    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("❌ Erros de validação:")
        for err in errors:
            print(f" - {err}")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    full_prompt_name = f"{username}/bug_to_user_story_v2"

    success = push_prompt_to_langsmith(full_prompt_name, prompt_data)

    if success:
        print(f"\n🚀 Prompt publicado em:")
        print(f"https://smith.langchain.com/hub/{username}/bug_to_user_story_v2")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
