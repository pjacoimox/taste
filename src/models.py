"""Modelo de dados e carregamento do CSV de restaurantes."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from .config import CSV_ENCODING


@dataclass
class Restaurante:
    nome: str
    bairro: str
    cozinha: str
    instagram: str = ""
    emoji: str = ""
    destaque: str = ""

    @property
    def tem_instagram(self) -> bool:
        return bool(self.instagram.strip())

    @property
    def instagram_ok(self) -> bool:
        """True se o @ está preenchido e no formato esperado."""
        h = self.instagram.strip()
        return h.startswith("@") and len(h) > 1


@dataclass
class Curadoria:
    restaurantes: list[Restaurante] = field(default_factory=list)

    def faltando_instagram(self) -> list[Restaurante]:
        return [r for r in self.restaurantes if not r.instagram_ok]

    def primeiros(self, n: int) -> list[Restaurante]:
        return self.restaurantes[:n]


def carregar_csv(caminho: str | Path) -> Curadoria:
    """Lê o CSV e devolve uma Curadoria.

    Colunas esperadas: nome, bairro, cozinha, instagram, emoji, destaque.
    Apenas nome e bairro são obrigatórios.
    """
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho}")

    restaurantes: list[Restaurante] = []
    with caminho.open(encoding=CSV_ENCODING, newline="") as f:
        leitor = csv.DictReader(f)
        for i, linha in enumerate(leitor, start=2):  # linha 1 é o cabeçalho
            nome = (linha.get("nome") or "").strip()
            bairro = (linha.get("bairro") or "").strip()
            if not nome or not bairro:
                print(f"  [aviso] linha {i} ignorada (sem nome ou bairro)")
                continue
            restaurantes.append(
                Restaurante(
                    nome=nome,
                    bairro=bairro,
                    cozinha=(linha.get("cozinha") or "").strip(),
                    instagram=(linha.get("instagram") or "").strip(),
                    emoji=(linha.get("emoji") or "").strip(),
                    destaque=(linha.get("destaque") or "").strip(),
                )
            )
    return Curadoria(restaurantes=restaurantes)
