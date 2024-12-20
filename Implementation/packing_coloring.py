from sage.all import *




def barvanje(G):
    """
    Calculates the packing coloring number for the given graph G
    """
    V = G.vertices()
    k = len(V)  # Maximum number of labels

    # Initialize the ILP
    ilp = MixedIntegerLinearProgram(maximization=False)
    x = ilp.new_variable(binary=True)  # Binary variables x_{v, i}
    z = ilp.new_variable(real=True)    # Continuous variable z

    # Objective: Minimize z
    ilp.set_objective(z[0])

    # Constraint 1: \sum_{i=1}^k x_{v, i} = 1 for all v in V
    for v in V:
        ilp.add_constraint(sum(x[v, i] for i in range(1, k + 1)) == 1)

    # Constraint 2: x_{v, i} + x_{u, i} <= 1 for all pairs (v, u) in V where d(v, u) <= i
    for v in V:
        for u in V:
            if v != u:
                d = G.distance(v, u)  # Calculate the distance between v and u
                for i in range(1, k + 1):
                    if d <= i:
                        ilp.add_constraint(x[v, i] + x[u, i] <= 1)

    # Constraint 3: i * x_{v, i} <= z for all v in V and i in {1, ..., k}
    for v in V:
        for i in range(1, k + 1):
            ilp.add_constraint(i * x[v, i] <= z[0])

    # Solve the ILP
    ilp.solve()
    
    return ilp.get_values(z[0])




def barvanje_ucinkovito(graph):
    """
    Calculates the packing coloring number for the given graph G. More efficient that function barvanje
    """
    # Variables
    vertices = graph.vertices()
    D = len(vertices)  # Maximum number of colors
    V = len(vertices)  # Number of vertices in G

    # Create a MixedIntegerLinearProgram instance
    ilp = MixedIntegerLinearProgram(maximization=False)
    x = ilp.new_variable(binary=True)

    # Objective function
    obj = V + D - 1 - sum(x[v, i] for v in vertices for i in range(1, D))
    ilp.set_objective(obj)

    # Constraints
    # 1. Each vertex is assigned exactly one color
    for v in vertices:
        ilp.add_constraint(sum(x[v, i] for i in range(1, D + 1)) == 1)

    # 2. Ensure distance constraints for the packing-coloring condition
    for i in range(1, D):
        for v in vertices:
            for u in vertices:
                if u != v and graph.distance(v, u) <= i:
                    ilp.add_constraint(x[v, i] + x[u, i] <= 1)

    # Solve the ILP
    ilp.solve()

    return ilp.get_objective_value()