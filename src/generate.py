"""Gera o briefing de um carrossel a partir de um CSV de restaurantes.

Uso:
    python -m src.generate --csv data/exemplo_restaurantes.csv \
        --tema "novidades de SP pra salvar" --n 10

Saída: um arquivo markdown em output/ pronto pra usar como briefing.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import HANDLE_TASTEWAY, HASHTAGS, TOM, CSV_ENCODING
from .models import carregar_csv

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATES = RAIZ / "templates"
SAIDA = RAIZ / "output"


def _slug(texto: str) -> str:
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-") or "carrossel"


def gerar(csv_path: str, tema: str, n: int) -> Path:
    curadoria = carregar_csv(csv_path)
    selecionados = curadoria.primeiros(n)
    if not selecionados:
        raise SystemExit("Nenhum restaurante válido no CSV.")

    n_real = len(selecionados)
    faltando = [r.nome for r in selecionados if not r.instagram_ok]

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("carrossel.md.j2")

    conteudo = template.render(
        tema=tema,
        tema_capa=tema,
        n=n_real,
        total_cards=n_real + 2,
        restaurantes=selecionados,
        handle=HANDLE_TASTEWAY,
        tom=TOM,
        hashtags=" ".join(HASHTAGS),
        faltando=", ".join(faltando),
    )

    SAIDA.mkdir(exist_ok=True)
    data = dt.date.today().isoformat()
    destino = SAIDA / f"carrossel_{_slug(tema)}_{data}.md"
    destino.write_text(conteudo, encoding=CSV_ENCODING)
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera briefing de carrossel TasteWay.")
    parser.add_argument("--csv", required=True, help="Caminho do CSV de restaurantes.")
    parser.add_argument("--tema", required=True, help='Tema, ex: "novidades de SP pra salvar".')
    parser.add_argument("--n", type=int, default=10, help="Quantas casas no carrossel (padrão 10).")
    args = parser.parse_args()

    destino = gerar(args.csv, args.tema, args.n)
    print(f"✓ Briefing gerado: {destino}")
    curadoria = carregar_csv(args.csv)
    faltando = [r.nome for r in curadoria.primeiros(args.n) if not r.instagram_ok]
    if faltando:
        print(f"  ⚠ Confirmar @ do Instagram: {', '.join(faltando)}")


if __name__ == "__main__":
    main()
