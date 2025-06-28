import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile
import os
import streamlit.components.v1 as components

nodes = pd.read_csv('nodes.csv')
edges = pd.read_csv('edges.csv')

artistas_pop = nodes[nodes['genres'].str.contains('pop', case=False, na=False)]

artistas_pop = artistas_pop.sort_values(by='popularity', ascending=False).head(100)
id_artistas_pop = artistas_pop['spotify_id'].unique()

pop_edges = edges[edges['id_0'].isin(id_artistas_pop) & edges['id_1'].isin(id_artistas_pop)]

G = nx.Graph()

for _, row in artistas_pop.iterrows():
    G.add_node(row['spotify_id'], name=row['name'], genre=row['genres'], popularity=row['popularity'])

for _, row in pop_edges.iterrows():
    G.add_edge(row['id_0'], row['id_1'], weight=row.get('weight', 1))

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

st.subheader("Centralidades")
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

top_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
st.markdown("**Top 10 Artistas por Centralidade de Grau:**")
for node, centrality in top_degree_centrality:
    st.markdown(f"- {G.nodes[node]['name']}: {centrality:.2f}")

st.subheader("Grafo Interativo com Pyvis")

net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

for node, data in G.nodes(data=True):
    net.add_node(node, label=data['name'],
                 title=f"<b>{data['name']}</b><br><br>Popularidade: {data['popularity']}",
                 size=data['popularity'] / 2)

for source, target, data in G.edges(data=True):
    net.add_edge(source, target)

with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    path = tmp_file.name
    net.save_graph(path)

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()
    components.html(html, height=650)