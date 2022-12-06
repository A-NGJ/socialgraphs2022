import matplotlib.pyplot as plt
import networkx as nx
import powerlaw

from style import style

# pylint: disable=too-many-arguments
def plot_graph_with_positons(
    graph: nx.Graph,
    positions,
    title,
    edge_color=style.Color.GRAY,
    node_color=style.Color.BLUE,
    node_alpha=0.8,
    edge_alpha=0.1,
):
    node_size = [graph.degree(node) // 3 for node in graph.nodes]
    _, ax = plt.subplots(1, 1, figsize=(15, 8))
    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=node_size,
        node_color=node_color,
        alpha=node_alpha,
        ax=ax,
    )
    nx.draw_networkx_edges(
        graph, positions, edge_color=edge_color, alpha=edge_alpha, ax=ax
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
    fig :
        Figure with degree distributions
    ax :
        Axes with degree distributions
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

    return fig, ax


# Aleks: Funkcja powinna zwracac In degree slope wg. docstringa, a jedynie printuje ta wartosc
# Lepiej jest ja zwrocic i uzyc printa juz poza funkcja
def power_law_fit(graph):
    """
    Calculate the best fit power law

    Returns
    -------
    In degree slope
    """
    in_degrees = [degree[1] for degree in graph.in_degree() if degree[1] > 0]
    return powerlaw.Fit(in_degrees).alpha


# Aleks: Ta funkcja akceptuje data jedynie w bardzo konkretnym formacie, dla naszego projektu ok, ale lepiej jest dodać
# dodatkowe parametry takie jak e.g. connection_column = "Crosslinks", node_name_column = "Name"
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


# Aleks: W docstringu jest directed graph, a zwracala wczesniej undirected graph. Zmienilem zwracana wartosc na directed
# bo w kazdym momencie mozna wywolac metode to_undirected() na zwrocnej wartosci, a w druga strone juz ciezej
def connected_components(graph: nx.Graph):
    """
    Extract large connected components

    Returns
    -------
    Directed graph
    """
    largest_component = sorted(
        nx.weakly_connected_components(graph), key=len, reverse=True
    )[0]
    directed_universe_lc = graph.subgraph(largest_component)
    return directed_universe_lc
