"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchainhub import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    client = Client()

    prompt_name = "leonanluppi/bug_to_user_story_v1"
    print(f"Fazendo pull do prompt: {prompt_name}...")

    prompt = client.pull(prompt_name)

    return prompt

def main():
    print_section_header("PULL DE PROMPTS DO LANGSMITH")

    # ✅ agora correto
    check_env_vars([
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT",
        "USERNAME_LANGSMITH_HUB"
    ])

    prompt = pull_prompts_from_langsmith()

    output_path = Path("prompts/bug_to_user_story_v1.yml")

    save_yaml(prompt, output_path)

    print(f"✅ Prompt salvo com sucesso em: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
