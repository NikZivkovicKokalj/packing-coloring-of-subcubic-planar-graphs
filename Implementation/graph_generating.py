import random

from sage.graphs.graph_generators import graphs
from sage.all import *




def removable_vertices(G):
    """
    Returns list of vertices that can be removed while maintaining connectivity of a graph
    """
    removable = []
    
    for v in G.vertices():
        H = G.copy()
        H.delete_vertex(v)  
        
        if H.is_connected():  
            removable.append(v)
    
    return removable




def modify_planar_subcubic_graph(G):
    """
    Modify a planar subcubic graph G while ensuring the number of vertices remains constant.
    """
    # copy of the graph to avoid modifying the input graph directly
    G = G.copy()
    
    # ensure the graph is planar and subcubic
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
