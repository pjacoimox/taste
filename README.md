# tasteway-content-kit

Toolkit de curadoria de conteúdo da TasteWay. Pega um CSV de restaurantes + um tema e gera o **briefing do carrossel pronto** (capa, card por card, legenda e checklist) em markdown — no tom da marca, em português.

Automatiza o fluxo: **pesquisa → curadoria (CSV) → briefing → produção de arte**.

## Como funciona

```
data/restaurantes.csv  ──►  src/generate.py  ──►  output/carrossel_*.md
        (curadoria)            (template)            (briefing pronto)
```

## Instalação

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Uso básico

```bash
python -m src.generate \
  --csv data/exemplo_restaurantes.csv \
  --tema "novidades de SP pra salvar" \
  --n 10
```

Saída em `output/carrossel_<tema>_<data>.md`, com:
- copy slide a slide (capa + N casas + CTA);
- legenda pronta com os @ e hashtags;
- checklist do que confirmar antes de publicar (inclusive @ que faltam).

## Formato do CSV

Colunas (só `nome` e `bairro` são obrigatórias):

| coluna     | exemplo                                   |
|------------|-------------------------------------------|
| nome       | Lena                                      |
| bairro     | Pinheiros                                 |
| cozinha    | Mineira contemporânea                     |
| instagram  | @lenaemsp                                 |
| emoji      | 🧀                                         |
| destaque   | Pão de queijo folhado e galinhada...      |

> Salve o CSV em **utf-8-sig** para abrir certo no Excel com acentos.

## Reescrever a copy no tom da marca (opcional)

`src/enrich.py` usa a API da Anthropic para reescrever os destaques no tom
descontraído/aconchegante. Precisa da chave em variável de ambiente:

```bash
export ANTHROPIC_API_KEY=...   # nunca comite a chave
pip install anthropic
python -m src.enrich --csv data/exemplo_restaurantes.csv
```

Gera `data/<arquivo>_enriquecido.csv`, que você passa para o `generate.py`.

## Personalização

- `src/config.py` — @ oficial da marca, hashtags padrão, paleta da identidade.
- `templates/carrossel.md.j2` — estrutura e textos fixos do carrossel
  (edite aqui para mudar capa, CTA ou legenda sem tocar no código).

## Próximos passos sugeridos

- [ ] Validação automática de @ do Instagram (checar se o perfil existe).
- [ ] Enriquecimento de endereço/avaliação via Google Places.
- [ ] Exportar também um CSV "pronto pra arte" para o Canva/Figma.
- [ ] Comando para abrir uma task no Notion com o briefing no corpo.
