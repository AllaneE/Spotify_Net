# Spotify_Net

Uma aplicação desenvolvida com Streamlit para analisar e visualizar redes de colaboração entre artistas dos gêneros **Trap**, **Rap** e **Hip-Hop**, com base em dados do Spotify.

## Sobre o Projeto

A aplicação realiza uma análise exploratória de redes a partir de dois arquivos:

- `nodes.csv`: contém os dados dos artistas (nome, ID do Spotify, popularidade, gêneros, etc.);
- `edges.csv`: contém as colaborações entre artistas, representadas por pares de IDs (`id_0`, `id_1`).

---

## Funcionalidades

- Filtragem de artistas dos gêneros **trap**, **rap** e **hip-hop**
- Seleção dos 250 artistas mais populares
- Construção do grafo com NetworkX
- Cálculo de métricas estruturais:
  - Número de nós e arestas
  - Densidade
  - Assortatividade
  - Clustering
  - Componentes conectados
- Histograma da distribuição de grau
- Cálculo e ranking de centralidades:
  - Degree
  - Betweenness
  - Closeness
  - Eigenvector
- Visualização interativa com Pyvis diretamente no Streamlit

---

## Como Executar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/AllaneE/Spotify_Net.git
cd Spotify_Net
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
streamlit run app.py
```
