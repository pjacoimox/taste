"""Opcional: reescreve os destaques no tom da marca usando a API da Anthropic.

Requer a variável de ambiente ANTHROPIC_API_KEY e o pacote `anthropic`.
Se a chave não estiver setada, o script avisa e não faz nada — o resto do
kit funciona normalmente sem isso.

Uso:
    export ANTHROPIC_API_KEY=...   # nunca comite a chave no Git
    python -m src.enrich --csv data/exemplo_restaurantes.csv
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

from .config import CSV_ENCODING, TOM
from .models import carregar_csv

CAMPOS = ["nome", "bairro", "cozinha", "instagram", "emoji", "destaque"]


def _reescrever_destaque(client, nome: str, cozinha: str, destaque: str) -> str:
    prompt = (
        f"Reescreva esta frase de divulgação de um restaurante em UMA linha curta "
        f"(máx. 22 palavras), tom {TOM}, sem emoji e sem aspas. "
        f"Restaurante: {nome} ({cozinha}). Frase original: {destaque}"
    )
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    partes = [b.text for b in resp.content if getattr(b, "type", "") == "text"]
    return " ".join(partes).strip() or destaque


def enriquecer(csv_path: str) -> Path:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "ANTHROPIC_API_KEY não definida. Defina a variável de ambiente para usar o enrich."
        )
    try:
        import anthropic
    except ImportError:
        raise SystemExit("Pacote 'anthropic' não instalado. Rode: pip install anthropic")

    client = anthropic.Anthropic()
    curadoria = carregar_csv(csv_path)

    for r in curadoria.restaurantes:
        if r.destaque:
            r.destaque = _reescrever_destaque(client, r.nome, r.cozinha, r.destaque)
            print(f"  ✓ {r.nome}")

    destino = Path(csv_path).with_name(Path(csv_path).stem + "_enriquecido.csv")
    with destino.open("w", encoding=CSV_ENCODING, newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for r in curadoria.restaurantes:
            w.writerow({
                "nome": r.nome, "bairro": r.bairro, "cozinha": r.cozinha,
                "instagram": r.instagram, "emoji": r.emoji, "destaque": r.destaque,
            })
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(description="Reescreve destaques no tom da marca (Anthropic).")
    parser.add_argument("--csv", required=True)
    args = parser.parse_args()
    destino = enriquecer(args.csv)
    print(f"✓ CSV enriquecido: {destino}")


if __name__ == "__main__":
    main()
