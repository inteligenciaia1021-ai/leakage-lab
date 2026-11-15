# Leakage Lab

![Testes](https://github.com/inteligenciaia1021-ai/leakage-lab/actions/workflows/tests.yml/badge.svg)

Experimento sobre **vazamento de dados** em machine learning: com dados sem
padrão nenhum, o procedimento errado leva um modelo a ~88% de acerto; o
correto fica perto de 50%.

- **Página com os resultados:** https://inteligenciaia1021-ai.github.io/leakage-lab/
- **Artigo:** https://www.linkedin.com/pulse/fiz-um-modelo-acertar-88-em-dados-sem-padr%C3%A3o-nenhum-artur-gomes-iu5re/

## A pergunta

Um modelo pode parecer ótimo sem ter aprendido nada? Sim, quando informação
do conjunto de teste participa da preparação do treino. Aqui, os dados são
puro ruído, então qualquer nota acima de ~50% é ilusão.

## O experimento

- 100 amostras, 5.000 colunas de ruído, rótulos sorteados
- Seleção das 20 colunas "mais promissoras" (`SelectKBest`)
- **Errado:** seleciona as colunas com todos os dados, depois valida
- **Certo:** a seleção acontece dentro de cada rodada da validação cruzada
  (5 folds), usando um `Pipeline`
- 50 repetições com sementes diferentes (0 a 49)

## Resultados

| | Média | Mínimo | Máximo | Desvio |
|---|---:|---:|---:|---:|
| Com vazamento | 88,0% | 82% | 92% | 2,9 |
| Sem vazamento | 50,7% | 39% | 64% | 5,9 |

Nas 50 repetições, a pior nota com vazamento (82%) superou a melhor nota
sem vazamento (64%).

## Formato dos resultados

O experimento grava `site/resultados.json`:

```jsonc
{
  "configuracao": {
    "amostras": 100,
    "colunas": 5000,
    "colunas_selecionadas": 20,
    "folds": 5,
    "repeticoes": 50
  },
  "com_vazamento": {
    "notas": [ /* 50 valores */ ],
    "media": 0.8804,
    "minimo": 0.82,
    "maximo": 0.92,
    "desvio": 0.0285
  },
  "sem_vazamento": {
    "notas": [ /* 50 valores */ ],
    "media": 0.5068,
    "minimo": 0.39,
    "maximo": 0.64,
    "desvio": 0.0591
  }
}
```

## Como rodar

Testado com Python 3.13.

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Depois, em qualquer sistema:

```bash
python src/experimento.py   # gera site/resultados.json
python -m pytest            # roda os testes
```

## Reproduzir o gráfico

A página lê o `resultados.json`, então precisa ser aberta por um servidor
local (abrir o `index.html` com dois cliques não funciona):

```bash
cd site
python -m http.server 8000 --bind 127.0.0.1
```

Abra http://localhost:8000. O gráfico é desenhado em SVG por `site/app.js`.
As sementes são fixas, então, com as versões do `requirements.txt`, os
resultados devem se repetir; versões diferentes de NumPy ou scikit-learn
podem causar pequenas variações numéricas.

## Testes

5 testes, cobertura de 68% de `experimento.py`. A parte não coberta é a
função `main()`, que grava o arquivo de resultados; a lógica do experimento
(`rodar_uma_vez`, `resumo`) está testada, incluindo reprodutibilidade e as
duas conclusões do experimento.

## Limitações

- Dados sintéticos de puro ruído, um único tipo de vazamento (seleção de
  variáveis) e um único modelo (regressão logística).
- O resultado mostra que o mecanismo existe e é grande neste cenário; não
  mede quanto ele infla notas em projetos reais.

## Estrutura

```text
src/experimento.py    experimento em Python
tests/                testes com pytest
site/                 página (HTML, CSS, JavaScript)
.github/workflows/    testes e publicação automáticos
```

## Autor

Artur Gomes · [LinkedIn](https://www.linkedin.com/in/artur-gomes-a2712a229/)