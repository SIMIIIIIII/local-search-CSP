"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

import random
from lsnode import LSNode
from atom_placement import AtomPlacement


def random_walk(problem, limit=100) -> LSNode:
    """
    Perform a random walk in the search space and returns a LSNode corresponding to the best found solution.
    """


    current = LSNode(problem, problem.init_state(), 0)
    best = current
    for step in range(limit):
        current = random.choice(list(current.expand()))
        if current.value() < best.value():
            best = current
    return best


def max_value(problem: AtomPlacement, limit=100) -> LSNode:
    """
    Perform a local search by selecting at each iteration the best neighbor of the current state.
    Returns a LSNode corresponding to the best found solution
    """

    current = LSNode(problem, problem.init_state(), 0)
    best = current
    
    for step in range(limit):
        neighbors = list(current.expand())
        if not neighbors:
            break
        
        next_node = min(neighbors, key=lambda n: n.value())
        current = next_node
        
        if current.value() < best.value():
            best = current
            
    return best


def randomized_max_value(problem: AtomPlacement, limit=100) -> LSNode:
    """
    Perform a local search by randomly selecting a neighbor among the 5 bests
    at each iteration.
    Returns a LSNode corresponding to the best found solution
    """
    current = LSNode(problem, problem.init_state(), 0)
    best = current
    
    for step in range(limit):
        neighbors = list(current.expand())
        if not neighbors:
            break
        
        sorted_neighbors = sorted(neighbors, key=lambda n: n.value())
        
        top_5 = sorted_neighbors[:min(5, len(sorted_neighbors))]
        
        next_node = random.choice(top_5)
        current = next_node
        
        if current.value() < best.value():
            best = current
            
    return best