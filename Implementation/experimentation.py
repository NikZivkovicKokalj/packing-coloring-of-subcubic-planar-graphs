import os
import random
import pickle
from itertools import islice

from sage.all import *
from sage.graphs.graph_generators import graphs

from Implementation.packing_coloring import *
from Implementation.graph_generating import *



########################################################################################################
##       Code for searching the highest PCN for graphs with up to 11 vertices using nauty_geng        ##
########################################################################################################

def save_state(filename, highest_value, best_graphs, start_iteration):
    """
    Save the state to a .pkl file.
    """
    state = {
        "highest_value": highest_value,
        "best_graphs": best_graphs,
        "start_iteration": start_iteration
    }
    with open(filename, "wb") as f:
        pickle.dump(state, f)




def load_state(filename):
    """
    Load the saved state from a .pkl file.
    """
    with open(filename, "rb") as f:
        return pickle.load(f)
    



def complete_search(m=100, state_file="graph_state.pkl"): 
    highest_value = 0
    best_graphs = []

    try:
        state = load_state(state_file)
        highest_value = state["highest_value"]
        best_graphs = state["best_graphs"]
        start_iteration = state["start_iteration"] 
        print(f"Resuming from iteration {start_iteration} with max coloring value {highest_value}.")
    except FileNotFoundError:
        start_iteration = 1
        print("No saved state found. Starting from scratch.")

    for n in range(start_iteration, m): 

        print(f"Starting iteration: {n}")

        for (i, G) in enumerate(graphs.nauty_geng(f"{n} -c")): 

            print(f"Looking at graph {i} with {n} vertices")

            if G.is_planar() and max(G.degree(v) for v in G.vertices()) <= 3: 
                packing_coloring_number = packing_coloring(G)
                if packing_coloring_number > highest_value:
                    print(f"Graph has the PCN: {packing_coloring_number}")
                    highest_value = packing_coloring_number
                    best_graphs = [G]

                elif packing_coloring_number == highest_value:
                    print(f"Graph has the PCN: {packing_coloring_number}")
                    best_graphs.append(G)

            else: print("Graph is not planar.")
        
        save_state(state_file, highest_value, best_graphs, n)
        print(f"State saved at iteration {n}.")
    




def display_best_graphs(state_file="graph_state.pkl"):
    state = load_state(state_file)

    # Extract relevant data
    highest_value = state["highest_value"]
    best_graphs = state["best_graphs"]

    # Print information about the graphs
    print(f"Maximum packing coloring value: {highest_value}")
    print(f"Number of saved graphs: {len(best_graphs)}")

    # Display each graph
    for idx, graph in enumerate(best_graphs, start=1):
        print(f"Displaying graph #{idx} with max coloring value {highest_value}...")
        graph.show(title=f"Graph #{idx} with value {highest_value}")
