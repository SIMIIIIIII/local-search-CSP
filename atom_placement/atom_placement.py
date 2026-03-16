"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

from atom_placement_state import AtomPlacementState


class AtomPlacement:

    # An init state building is provided here but you can change it at will
    def init_state(self) -> AtomPlacementState:
        sites = []
        for atom_type, quantity in enumerate(self.n_types):
            for i in range(quantity):
                sites.append(atom_type)

        return AtomPlacementState(sites)

    # Returns the neighbor states of the given state as a list of AtomPlacementState
    def neighbors(self, state: AtomPlacementState) -> list[AtomPlacementState]:

        neighbors = []
        arr = state.sites_assignment
        n = len(arr)

        for i in range(n):
            for j in range(i + 1, n):

                if arr[i] != arr[j]:

                    new_assignment = arr.copy()
                    new_assignment[i], new_assignment[j] = new_assignment[j], new_assignment[i]

                    neighbors.append(AtomPlacementState(new_assignment))

        return neighbors

    # Returns the objective value of the given state
    def value(self, state: AtomPlacementState) -> int:
        res = 0

        for edge in self.edges:
            i = state.sites_assignment[edge[0]]
            j = state.sites_assignment[edge[1]]
            res += self.energy_matrix[i][j]

        return res

    def __init__(self, filename: str):
        file = open(filename)
        line = file.readline()
        self.n_sites = int(line.split(' ')[0])
        self.k = int(line.split(' ')[1])
        self.n_edges = int(line.split(' ')[2])
        self.edges = []
        file.readline()

        self.n_types = [int(val) for val in file.readline().split(' ')]
        if sum(self.n_types) != self.n_sites:
            print('Invalid instance, wrong number of sites')
        file.readline()

        self.energy_matrix = []
        for i in range(self.k):
            self.energy_matrix.append([int(val) for val in file.readline().split(' ')])
        file.readline()

        for i in range(self.n_edges):
            self.edges.append([int(val) for val in file.readline().split(' ')])


if __name__ == "__main__":
    a = AtomPlacement("instances/i01.txt")
    s = a.init_state()
    n = a.neighbors(s)

    v = [a.value(st) for st in n]
    print(v)