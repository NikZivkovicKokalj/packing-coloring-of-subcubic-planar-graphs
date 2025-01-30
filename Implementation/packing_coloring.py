from sage.graphs.graph_generators import graphs
from sage.all import *




def packing_coloring(graph):
    """
    Calculates the packing coloring number for the given graph.
    """
    # Variables
    vertices = graph.vertices()
    diameter = graph.diameter()  
    D = diameter + 1  # max possible colors

    ilp = MixedIntegerLinearProgram(maximization=False)
    x = ilp.new_variable(binary=True)
    k = ilp.new_variable(real=True, nonnegative=True)

    # minimizing max color index
    ilp.set_objective(k[0])  

    # Constraints
    # each vertex only 1 color
    for v in vertices:
        ilp.add_constraint(sum(x[v, i] for i in range(1, D + 1)) == 1)

    # vertices with the same color must satisfy the distance 
    for i in range(1, D + 1):
        for v in vertices:
            for u in vertices:
                if u != v and graph.distance(v, u) < i + 1:
                    ilp.add_constraint(x[v, i] + x[u, i] <= 1)

    # `k[0]` must capture max color index used
    for i in range(1, D + 1):
        for v in vertices:
            ilp.add_constraint(k[0] >= i * x[v, i])

    ilp.solve()
    packing_number = int(ilp.get_objective_value())

    return packing_number
