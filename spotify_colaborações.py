import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile
import matplotlib.pyplot as plt
import os
import streamlit.components.v1 as components

nodes = pd.read_csv('nodes.csv')
edges = pd.read_csv('edges.csv')

artistas = nodes.sort_values(by='popularity', ascending=False).head(400)
id_artistas = artistas['spotify_id'].unique()

edges = edges[edges['id_0'].isin(id_artistas) & edges['id_1'].isin(id_artistas)]

G = nx.Graph()

for _, row in artistas.iterrows():
    G.add_node(row['spotify_id'], name=row['name'], genre=row['genres'], popularity=row['popularity'])

for _, row in edges.iterrows():
    G.add_edge(row['id_0'], row['id_1'])

node_labels = nx.get_node_attributes(G, 'name')
print('nós', G.number_of_nodes())
print('arestas', G.number_of_edges())

densidade = nx.density(G)
assortabilidade = nx.degree_assortativity_coefficient(G)
clustering = nx.average_clustering(G)
conectados = list(nx.connected_components(G))

st.title("Grafo de Colaboração de Artistas do Gênero Pop")
st.subheader("Informações da Rede")
st.markdown(f"**Densidade**: {densidade:.2f}")
st.markdown(f"**Assortatividade**: {assortabilidade:.2f}")
st.markdown(f"**Coeficiente de Clustering**: {clustering:.2f}")
st.markdown(f"**Número de Componentes Conectados**: {len(conectados)}")

st.subheader("Distribuição do Grau dos Nós")
degree_sequence = [d for n, d in G.degree()]
fig, ax = plt.subplots()
ax.hist(degree_sequence, bins=range(1, max(degree_sequence)+2), color='skyblue', edgecolor='black')
ax.set_title("Distribuição de Grau dos Nós")
ax.set_xlabel("Grau")
ax.set_ylabel("Quantidade de Nós")
st.pyplot(fig)

st.subheader("Ranking de Centralidades")
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
try:
    eigenvector_centrality = nx.eigenvector_centrality(G)
except nx.PowerIterationFailedConvergence:
    eigenvector_centrality = {n: 0 for n in G.nodes}

centralidades = {
    "Degree Centrality": degree_centrality,
    "Betweenness Centrality": betweenness_centrality,
    "Closeness Centrality": closeness_centrality,
    "Eigenvector Centrality": eigenvector_centrality
}

# Interface para escolher métrica
metrica = st.selectbox("Escolha a métrica de centralidade:", list(centralidades.keys()))
top_k = 10
ranking = sorted(centralidades[metrica].items(), key=lambda x: x[1], reverse=True)[:top_k]

st.markdown(f"**Top {top_k} Artistas por {metrica}:**")
for i, (node, valor) in enumerate(ranking, 1):
    nome = G.nodes[node]['name']
    st.markdown(f"{i}. **{nome}** — {valor:.4f}")

st.subheader("Grafo Interativo com Pyvis")

net = Network(height="750px", width="100%", bgcolor="#FFFFF", font_color="black")

for node, data in G.nodes(data=True):
    net.add_node(node, label=data['name'], title=f"<b>{data['name']}</b><br><br>Popularidade: {data['popularity']}", size=data['popularity']/2)

for source, target, data in G.edges(data=True):
    net.add_edge(source, target)

net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "springLength": 700
    }
  }
}
""")

with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    path = tmp_file.name
    net.save_graph(path)

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()
    components.html(html, height=650)
