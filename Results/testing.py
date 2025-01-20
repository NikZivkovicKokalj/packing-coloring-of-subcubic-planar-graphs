import random
import pickle
import os
from sage.all import *
from sage.graphs.graph_generators import graphs

from Implementation.packing_coloring import *
from Implementation.graph_generating import *




def save_state(filename, max_coloring_value, best_graphs, current_graph, iteration):
    """
    Save the state to a .pkl file.
    """
    state = {
        "max_coloring_value": max_coloring_value,
        "best_graphs": best_graphs,
        "current_graph": current_graph,
        "iteration": iteration
    }
    with open(filename, "wb") as f:
        pickle.dump(state, f)




def load_state(filename):
    """
    Load the saved state from a .pkl file.
    """
    with open(filename, "rb") as f:
        return pickle.load(f)
    



def main(iterations=100000, save_interval=1000, state_file="graph_state.pkl"):
    """
    Main program to apply transformations and find graphs with the largest packing coloring number.
    """
    max_coloring_value = 0
    best_graphs = []
    current_graph = None
    start_iteration = 0

    # Attempt to load the state if it exists
    try:
        state = load_state(state_file)
        max_coloring_value = state["max_coloring_value"]
        best_graphs = state["best_graphs"]
        current_graph = state["current_graph"]
        start_iteration = state["iteration"]
        print(f"Resuming from iteration {start_iteration} with max coloring value {max_coloring_value}.")
    except FileNotFoundError:
        print("No saved state found. Starting from scratch.")
        # Generate initial random planar subcubic graph
    while not current_graph:
        graph = graphs.RandomGNP(10, 0.3)
        subgraph = graph.subgraph(lambda x: graph.degree(x) <= 3)
        if subgraph.is_planar() and subgraph.is_connected():
            current_graph = subgraph

    # Start or continue iterations
    for i in range(start_iteration + 1, iterations + 1):
        # Calculate packing coloring number
        coloring_number = barvanje(current_graph)

        if coloring_number > max_coloring_value:
            max_coloring_value = coloring_number
            best_graphs = [current_graph.copy()]
        elif coloring_number == max_coloring_value:
            best_graphs.append(current_graph.copy())

        # Apply transformation
        current_graph = modify_planar_subcubic_graph(current_graph)

        # Save the state at intervals
        if i % save_interval == 0:
            save_state(state_file, max_coloring_value, best_graphs, current_graph, i)
            print(f"State saved at iteration {i}.")

    print(f"Highest packing coloring number achieved: {max_coloring_value}")
    print(f"Number of graphs with the highest packing coloring number: {len(best_graphs)}")

    # Create the "Results" folder if it doesn't exist
    results_folder = "Results"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # Save the best graphs into the "Results" folder
    for idx, best_graph in enumerate(best_graphs, start=1):
        filename = f"{results_folder}/best_graph_{idx}_color_{max_coloring_value}.graph.sobj"
        best_graph.save(filename)
        print(f"Graph #{idx} saved as {filename}")




# LOOKING AT THE BEST GRAPHS
state = load_state("graph_state.pkl")

# Extract relevant data
max_coloring_value = state["max_coloring_value"]
best_graphs = state["best_graphs"]

# Print information about the graphs
print(f"Maximum packing coloring value: {max_coloring_value}")
print(f"Number of saved graphs: {len(best_graphs)}")

# Display each graph
for idx, graph in enumerate(best_graphs, start=1):
    print(f"Displaying graph #{idx} with max coloring value {max_coloring_value}...")
    graph.show(title=f"Graph #{idx} with value {max_coloring_value}")

