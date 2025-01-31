import os
import random
import time
import pickle
from itertools import islice

from sage.all import *
from sage.graphs.graph_generators import graphs

from Implementation.packing_coloring import *
from Implementation.graph_generating import *







########################################################################################################
##       Code for searching the highest PCN for graphs with up to 11 vertices using nauty_geng        ##
########################################################################################################




def complete_search(m, k=100, state_file="graph_state.pkl"):
    """
    Parameters:
        m (int): Max number of vertices that are still completely searched.
        k (int, optional): Frequency of saving progress.
        state_file (str, optional): File path for saving state.
    """

    # Initialize or load state
    try:
        with open(state_file, "rb") as f:
            state = pickle.load(f)
        current_graph = state["current_graph"]
        highest_value = state["highest_value"]
        best_graphs = state["best_graphs"]
        start_iteration = state["start_iteration"] + 1
        print(f"Resuming from iteration {start_iteration}")
    except (FileNotFoundError, KeyError):
        current_graph = 5
        highest_value = 0
        best_graphs = []
        start_iteration = 0
        print("No saved state found. Starting from scratch.")

    # Process vertex counts from current_graph to m
    while current_graph <= m:
        print(f"\nProcessing graphs with {current_graph} vertices...")
        graph_generator = graphs.nauty_geng(f"{current_graph} -c -D3 -p") 
        
        try:
            # Track progress within the inner loop
            for i, G in islice(enumerate(graph_generator), start_iteration, None):
                if G.is_planar(): 
                    try:
                        packing_coloring_number = packing_coloring(G)
                    except: 
                        continue
                else: print("Graph is not planar.")

                print(f"Graph {i} has PCN of {packing_coloring_number}.")

                if packing_coloring_number > highest_value:
                    highest_value = packing_coloring_number
                    best_graphs = [G]

                elif packing_coloring_number == highest_value:
                    best_graphs.append(G)


                # Save state every k graphs processed for current_n
                if (i - start_iteration + 1) % k == 0:
                    save_state(state_file, highest_value, best_graphs, i + 1, current_graph)
                    print(f"Iteration {i}: Best PCN = {highest_value}. Looking at graphs with {current_graph} vertices")

                start_iteration = i

            # Finished all graphs for current_n: save and reset offset
            start_iteration = 0
            current_graph += 1
            save_state(state_file, highest_value, best_graphs, current_graph, start_iteration)
            print(f"Saved state after completing n={current_graph - 1}")

        except KeyboardInterrupt:
            # Save progress on interruption
            print("\nInterrupted! Saving state...")
            save_state(state_file, highest_value, best_graphs, start_iteration + 1, current_graph)
            break

    save_state(state_file, highest_value, best_graphs, start_iteration + 1, current_graph)
    
    print("DONE!")




def save_state(filename, highest_value, best_graphs, start_iteration, current_graph=None):
    """
    Save the state to a .pkl file.
    """
    state = {
        "current_graph": current_graph,
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




def display_best_graphs(n, state_file="graph_state.pkl"):
    """
    Displays n of the best graphs stored in the state_file
    """
    state = load_state(state_file)

    # Extract relevant data
    highest_value = state["highest_value"]
    best_graphs = state["best_graphs"]

    # Print information about the graphs
    print(f"Maximum packing coloring value: {highest_value}")
    print(f"Number of saved graphs: {len(best_graphs)}")

    # Display each graph
    for idx, graph in enumerate(best_graphs, start=1):
        if idx > n: 
            break
        print(f"Displaying graph #{idx} with max coloring value {highest_value}...")
        graph.show(title=f"Graph #{idx} with value {highest_value}")








########################################################################################################
##          Code for searching the highest PCN for graphs with over 12 vertices using while           ##
##                      modifying the graph with modify_planar_subcubic_graph                         ##
########################################################################################################




def initialize_base_graph(num_vertices):
    """
    Generates a single planar subcubic graph using nauty_geng
    """
    # Use filters to choose a planar, connected and subcubic graph 
    gen = graphs.nauty_geng(f"{num_vertices} -c -D3 -p")  
    G = next(gen)

    while True: 
        if G.is_planar(): 
            return G
        G = next(gen)
        




def random_search(num_vertices, iterations, save_interval=100, state_file="graph_state.pkl"):
    """  
    Parameters:
        num_vertices (int): Number of vertices in the initial graph.
        iterations (int): Total number of iterations to run.
        save_interval (int, optional): Frequency of saving progress.
        state_file (str, optional): File path for saving state.
    """
    # Load state or initialize
    try:
        with open(state_file, "rb") as f:
            state = pickle.load(f)
        current_graph = state["current_graph"]
        highest_value = state["highest_value"]
        best_graphs = state["best_graphs"]
        start_iteration = state["start_iteration"] + 1
        print(f"Resuming from iteration {start_iteration}")
    except (FileNotFoundError, KeyError):
        current_graph = initialize_base_graph(num_vertices)
        highest_value = packing_coloring(current_graph)
        best_graphs = [current_graph]
        start_iteration = 0
        print("Initialized new search")

    # Keep track of all the seen graphs with a unique string
    seen = {current_graph.canonical_label().graph6_string()}

    iteration = start_iteration

    try:
        for iteration in range(start_iteration, iterations):
            # Modify the current graph
            modified_graph = modify_planar_subcubic_graph(current_graph)
            print(f"Modified graph number {iteration}")
            
            # Skip duplicates
            modified_hash = modified_graph.canonical_label().graph6_string()
            if modified_hash in seen:
                print("Graph has been already seen!")
                continue
            seen.add(modified_hash)

            # Calculate the PCN 
            try:
                current_value = packing_coloring(modified_graph)
            except: 
                continue
            print(f"Graph {iteration} has PCN of {current_value}.")
            
            if current_value > highest_value:
                highest_value = current_value
                best_graphs = [modified_graph]
            elif current_value == highest_value:
                best_graphs.append(modified_graph)

            # Always move to modified graph
            current_graph = modified_graph

            # Save progress periodically
            if iteration % save_interval == 0:
                save_state(state_file, highest_value, best_graphs, iteration, current_graph)
                print(f"Iteration {iteration}: Best PCN = {highest_value}")

    except KeyboardInterrupt:
        # Save progress on interruption
        print("\nProccess interrupted. Saving progress...")
        save_state(state_file, highest_value, best_graphs, iteration, current_graph)

    # Final save
    save_state(state_file, highest_value, best_graphs, iteration, current_graph)

    print("DONE!")




def measure_packing_coloring_time(n):
    """
    Measures average runtime of packing_coloring across graphs with 5-20 vertices.
    """
    results = []
    for num_vertices in range(5, 21):
        print(f"\nProcessing graphs with {num_vertices} vertices...")
        graph_generator = graphs.nauty_geng(f"{num_vertices} -c -D3 -p") 

        iteration = 0
        times = []
        
        try:
            # Track progress within the inner loop
            for G in graph_generator:
                if iteration > n:
                    break
                if G.is_planar(): 
                    try:
                        start = time.perf_counter()
                        packing_coloring(G)
                        end = time.perf_counter()

                        times.append(end - start)
                        iteration += 1
                    except: 
                        continue
                else: print("Graph is not planar.")

                print(f"Processed graph {iteration}")   

        except KeyboardInterrupt:
            # Save progress on interruption
            print("\nInterrupted!")
            return results

        avg_time = sum(times) / len(times)
        results.append((n, avg_time))
        print(f"n={num_vertices}: Avg time = {avg_time:.4f}s")

    return results
