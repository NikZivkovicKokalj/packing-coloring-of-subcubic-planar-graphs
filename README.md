# Packing Coloring of Subcubic Planar Graphs

## Introduction

Project for the FINP course at UL FMF.

We want to find a planar subcubic graph with the packing coloring number as large as possible.

In a packing coloring, we want to color vertices of a graph by colors $1,2,3, \ldots$ so that each pair of vertices of color $i$ is at distance $\geq i+1$. The smallest number of colors need to color a given graph in such a way is the packing coloring number of that graph, $\chi_\rho(G)$.

We implement an ILP model to determine the packing coloring number for a given graph and write various procedures to efficiently check the packing coloring numbers for a large number of graphs.

The results of our search are stored in the `Results` folder, and reports can be found in `.pdf` file within the `Long Presentation` and `Short Presentation` folders.

## Instructions for Usage 

All functions for running your own analysis are located in the `Implementation` folder. The main script to execute is `experimentation.py`, which contains multiple functions for studying packing coloring numbers. To use this repository, follow the instructions below:

### Prerequisites
Before running the scripts, ensure that you have **SageMath** installed on your computer. Link for installation: [Download SageMath](https://www.sagemath.org/).

### Running the Script
To execute the script, navigate to the repository's root directory and run the following command in your terminal:c
```bash
sage
```
```bash
load("Implementation/experimentation.py")
```


### Function Overview

#### Function 1: "complete_search(n)"
- This function iterates through *all* graphs up to a given number of vertices (n).
- It checks if each graph is subcubic, planar, and connected.
- If the graph meets the criteria, it calculates the packing coloring number.
- The function keeps track of the graphs with the *highest* packing coloring number and periodically saves them in a `.pkl` file at a user-defined interval.
- **Note:** On most computers this approach becomes **inefficient** for graphs with **12 or more vertices**, as the number of possible graphs grows exponentially.

#### Function 2: "random_search(n, iterations)"
- This function is useful for studying graphs with a **higher number of vertices** where an complete search approach is infeasible.
- It starts with a *randomly generated* graph (planar, subcubic and connected) with the specified number of vertices (n).
- In each iteration:
  - It calculates the packing coloring number.
  - It modifies the graph to maintain its subcubic, planar, and connected properties while keeping the number of vertices unchanged.
- The function keeps track of the graphs with the highest packing coloring number and saves them in a `.pkl` file at user-specified intervals.

#### Function 3: "display_best_graphs("file_name.pkl")"
- This function allow the user to extract and analyze graphs stored in `.pkl` files created by **complete_search** and **random_search** functions.
- This is useful for further investigation and visualization of graphs with high packing coloring numbers.


## Authors 
*Jon Pascal Miklavčič* and *Nik Živkovič Kokalj*.

## Advisers 
*Assist. Prof. Dr. Janoš Vidali* and *Prof. Dr. Riste Škrekovski*.