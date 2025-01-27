import random

from sage.graphs.graph_generators import graphs
from sage.all import *




def modify_planar_subcubic_graph(G):
    """
    Modify a planar subcubic graph G by adding a vertex into a randomly selected face, adding and removing edges while maintaining planarity, subcubic constraints and making sure that the graph is connected.
    """
    # ensure the graph is planar and subcubic
    if not G.is_planar():
        raise ValueError("The graph must be planar.")
    for v in G.vertices():
        if G.degree(v) > 3:
            raise ValueError("The graph must be subcubic.")
    if not G.is_connected():
        raise ValueError("The graph must be connected.")
    
    operation = random.choice(["add_vertex", "rewire_edge", "face"])
    
    if operation == "add_vertex":
        new_vertex = max(G.vertices()) + 1
        G.add_vertex(new_vertex) 
        random_edge = random.choice(G.edges(labels=False)) # random edge that will be removed
        a, b = random_edge
        G.add_edge(new_vertex, a) # adding 2 new edges from the new vertex to vertices between which the edge will be removed
        G.add_edge(new_vertex, b)
        G.delete_edge(random_edge) # deleting the edge but still maintaining conectivity of a graph
        
        

    elif operation == "rewire_edge":
    
        # deleting 2 edges
        deleted_edges = 0
        edges = list(G.edges(labels=False))
        while deleted_edges < 2:
            
            # if we for example have a cycle graph there will only be 1 connection that can be deleted while still maintaining graph connected
            if not edges:
                break
                
            r= random.choice(edges)
            t = G.copy()
            t.delete_edge(r)
            if t.is_connected():
                G.delete_edge(r)
                deleted_edges += 1
                edges.remove(r)
            else:
                edges.remove(r)
                
        # adding 2 edges           
        added_edges = 0
        vertices = G.vertices()
        while added_edges < 2:
            u, v = random.sample(vertices, 2)
            if not G.has_edge(u, v):              
                G.add_edge(u, v)
                if G.is_planar() and all(G.degree(v) <= 3 for v in G.vertices()):
                    added_edges += 1
                else:
                    G.delete_edge((u, v)) 
           
        
    
    elif operation == "face":
        
        faces = G.faces()

        if not faces:
            raise ValueError("The graph has no faces to modify.")

        # Randomly select a face f
        f = Graph(random.choice(faces)) # considering face of a graph as a new graph

        # list of vertices that are in selected face
        face_vertices = set(v for edge in f.edges(labels=False) for v in edge) # vozlisca ki so v novem grafu

        # adding a new vertex v
        new_vertex = max(f.vertices()) + 1
        f.add_vertex(new_vertex)

        # identifying vertices of degree ≤ 2 on the selected face as they are eligible to be connected to a new vertex
        eligible_vertices = [v for v in face_vertices if f.degree(v) <= 2]

        # if there is less than 2 vertices that can be connected to a new vertex, 2 of the existing edges are removed
        if len(eligible_vertices) < 2:
            random_edge = random.choice(f.edges(labels=False)) # random edge that will be removed
            a,b = random_edge
            f.add_edge(new_vertex,a) # adding 2 new edges from the new vertex to vertices between which the edge will be removed
            f.add_edge(new_vertex,b)
            f.delete_edge(random_edge) # deleting the edge but still maintaining conectivity of a graph

            # because only 1 edge was removed and 2 were added I am looking for another edge to be removed while maintaining conectivity of a graph. If there is none, only 1 edge will be removed and 2 will be added 
            edges = list(f.edges(labels=False))

            for _ in range(len(edges)):
                edge_to_remove = random.choice(edges)
                edges.remove(edge_to_remove) 
                f_copy = f.copy()
                f_copy.delete_edge(edge_to_remove)

                if f_copy.is_connected():
                    f.delete_edge(edge_to_remove)  
                    break 
            G = f
        else:
            # randomly select 2 or 3 eligible vertices to connect to new_vertex
            num_connections = random.randint(2, min(3, len(eligible_vertices)))
            chosen_vertices = random.sample(eligible_vertices, num_connections)

            for v in chosen_vertices:
                f.add_edge(new_vertex, v)
            print(f"Connected new vertex {new_vertex} to vertices: {chosen_vertices}")

            i = 1
            while i < num_connections:
                edge = random.sample(list(f.edges(labels=False)),1)[0]
                f_copy = f.copy()
                f_copy.delete_edge(edge)
                if f_copy.is_connected():
                    f.delete_edge(edge)
                    i += 1
                    G = f
            
        
    return G




def loop_find_max_coloring(G, modify_planar_subcubic_graph, iterations=1000000):
    """
    Performs a specified number of iterations, tracking graphs with the highest coloring value.
    """
    max_value = 0  
    best_graphs = [] 

    for _ in range(1, iterations + 1):

        # Calculate the number of colors for the current graph
        color_count = barvanje_ucinkovito(G)

        # If a new maximum value is reached, update max_value and save the graph
        if color_count > max_value:
            max_value = color_count
            best_graphs = [G.copy()]
        elif color_count == max_value:
            best_graphs.append(G.copy())
        G = modify_planar_subcubic_graph(G)

    print(f"\nHighest achieved value: {max_value}")
    print(f"Number of graphs with the highest value: {len(best_graphs)}")

    # Display all the best graphs
    for idx, best_G in enumerate(best_graphs, start=1):
        print(f"\nGraph #{idx} with value {max_value}:")
        best_G.show(title=f"Best graph #{idx} with value {max_value}")


#new graph generating function
def removable_vertices(G):
    """returns list of vertices that can be removed while maintaining connectivity of a graph"""
    removable = []
    
    for v in G.vertices():
        H = G.copy()
        H.delete_vertex(v)  
        
        if H.is_connected():  
            removable.append(v)
    
    return removable

import random

def modify_planar_subcubic_graph(G):
    """
    Modify a planar subcubic graph G while ensuring the number of vertices remains constant.
    """
    # copy of the graph to avoid modifying the input graph directly
    G = G.copy()
    
    # Ensure the graph is planar and subcubic
    if not G.is_planar():
        raise ValueError("The graph must be planar.")
    for v in G.vertices():
        if G.degree(v) > 3:
            raise ValueError("The graph must be subcubic.")
    
    

    faces = G.faces()  
    if not faces:
        return G

    face = random.choice(faces)  
    face_vertices = set([v for subface in face for v in subface])  
    

    num_subdivisions = random.randint(1, 3)
    for _ in range(num_subdivisions):
        face_edges = [
            edge for edge in G.edges(labels=False)
            if edge[0] in face_vertices and edge[1] in face_vertices
        ]

        if not face_edges: 
            break

        edge_to_subdivide = random.choice(face_edges)
        a, b = edge_to_subdivide

        new_sub_vertex = max(G.vertices()) + 1
        G.add_vertex(new_sub_vertex)
        G.add_edge(a, new_sub_vertex)
        G.add_edge(b, new_sub_vertex)
        G.delete_edge(a, b)

        face_vertices.add(new_sub_vertex)

        removable = removable_vertices(G)
        if removable:
            random_vertex = random.choice(removable)
            G.delete_vertex(random_vertex)
            if random_vertex in face_vertices:
                face_vertices.discard(random_vertex)
        else: 
            G.delete_vertex(new_sub_vertex)
            G.add_edge(a,b)


    
    eligible_vertices = [v for v in face_vertices if G.degree(v) <= 2]
    
    new_vertex = max(G.vertices()) + 1
    
    G.add_vertex(new_vertex)
    if eligible_vertices:
        num_new_edges = min(random.randint(1, 3), len(eligible_vertices))
        for _ in range(num_new_edges):
            target_vertex = random.choice(eligible_vertices)
            G.add_edge(new_vertex, target_vertex)
            eligible_vertices.remove(target_vertex)
            
        removable2 = removable_vertices(G)
        if new_vertex in removable2:
            removable2.remove(new_vertex)

        if removable2:
            random_vertex2 = random.choice(removable2)
            G.delete_vertex(random_vertex2)
        else:
            G.delete_vertex(new_vertex)
    else:
        G.delete_vertex(new_vertex)


    
    return G

