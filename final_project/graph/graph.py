from collections import Counter
import typing as t

from community import community_louvain
import matplotlib.pyplot as plt
import networkx as nx
import powerlaw

from style import style

# pylint: disable=too-many-arguments
def plot_graph_with_positons(
    graph: nx.Graph,
    positions,
    title,
    figsize=(15, 8),
    edge_color=style.Color.BLACK,
    node_color=style.Color.BLUE,
    node_alpha=0.8,
    node_size_factor=1,
    edge_alpha=0.1,
    labels=None,
    label_color=style.Color.BLACK,
    label_font_size=6,
    cmap=None,
):
    node_sizes = [graph.degree(node) * node_size_factor for node in graph.nodes]
    _, ax = plt.subplots(1, 1, figsize=figsize)
    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=node_sizes,
        node_color=node_color,
        alpha=node_alpha,
        ax=ax,
        cmap=cmap,
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color=edge_color,
        alpha=edge_alpha,
        ax=ax,
    )
    if labels:
        nx.draw_networkx_labels(
            graph,
            positions,
            labels=dict(labels),
            font_color=label_color,
            font_size=label_font_size,
            ax=ax,
        )
    ax.set_title(title, size=24)
    ax.axis("off")
    plt.tight_layout()
    plt.show()


# Aleks: Docstring ma Returns = Subplot..., a funkcja nic nie zwraca. Jedynie rysuje wykres.
# Dodalem fig, ax jako return values
def plot_degree_distribution(graph, scale=None):
    """
    Count the in/out degree distributions and visualize.
    If scale == log then the y-axis will be in log scale, else normal scale.

    Returns
    -------
    In degree
    Out degree
    """
    in_degrees = [d for _, d in graph.in_degree()]
    out_degrees = [d for _, d in graph.out_degree()]

    fig, ax = plt.subplots(1, 2, figsize=(12, 8))
    plt.suptitle("Degree distribution")
    ax[0].hist(in_degrees, bins=100, color="cornflowerblue")
    ax[0].set_xlabel("Degree")
    ax[0].set_title("In-degree")
    ax[0].grid("on")
    ax[1].hist(out_degrees, bins=100, color="cornflowerblue")
    if scale == "log":
        ax[0].set_yscale("log")
        ax[1].set_yscale("log")
        ax[0].set_ylabel("Count (log scale)")
    else:
        ax[0].set_ylabel("Count")
    ax[1].set_title("Out-degree")
    ax[1].set_xlabel("Degree")
    ax[1].grid("on")

    return in_degrees, out_degrees


def power_law_fit(graph):
    """
    Calculate the best fit power law

    Returns
    -------
    In degree slope
    """
    in_degrees = [degree[1] for degree in graph.in_degree() if degree[1] > 0]
    return powerlaw.Fit(in_degrees).alpha


def create_directed_graph(data):
    """
    Create directed graph based on data with parameters: Name, Gender, Species, Homeworld, Affiliations, Died

    Returns
    -------
    Directed graph
    """
    # initialize universe directional graph
    Universe = nx.DiGraph()
    for _, character in data.iterrows():
        # add node with metadata for each character
        Universe.add_node(
            character.Name,
            gender=character.Gender,
            species=character.Species,
            home=character.Homeworld,
            affiliations=character["Affiliation(s)"],
            died=character.Died,
        )
        for connection in character.Crosslinks:
            if connection in data.Name.values:
                # add edge between character and its connection if it's not a self loop
                if connection != character.Name:
                    Universe.add_edge(character.Name, connection)
    return Universe


def connected_components(graph: nx.Graph) -> nx.Graph:
    """
    Extract large connected components

    Returns
    -------
    Directed graph
    """
    if graph.is_directed():
        connected_components = nx.weakly_connected_components
    else:
        connected_components = nx.connected_components

    largest_component = sorted(connected_components(graph), key=len, reverse=True)[0]
    directed_universe_lc = graph.subgraph(largest_component)
    return directed_universe_lc


def find_communities(graph: nx.Graph) -> t.Tuple[dict, Counter, float]:
    """
    Finding the best partition of the graph

    Returns
    -------
    Best partition, communities, and modularity
    """
    # compute the best partition
    partition = community_louvain.best_partition(graph)
    # modularity
    mod = community_louvain.modularity(partition, graph, weight="weight")
    # number of communities
    communities = Counter(partition.values())
    return partition, communities, mod


def plot_communities(communities):
    """
    Plot the distribution of communities in the network
    """

    _ = plt.figure(figsize=(10, 6))
    plt.bar(communities.keys(), communities.values(), color="navy")
    plt.title("Communities in the Star Wars Universe")
    plt.xlabel("Communities")
    plt.ylabel("Count")
