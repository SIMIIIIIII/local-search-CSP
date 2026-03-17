"""NAMES OF THE AUTHOR(S): Alice Burlats <alice.burlats@uclouvain.be>"""

from pycsp3 import *


def solve_minesweeper(clues: list[list[int]]) -> list[(int, int)]:
    clear()   
    
    n = len(clues)
    m = len(clues[0])

    
    x = VarArray(size=[n, m], dom={0, 1})

    contraintes = []

    # toutes les cases avec un indice dessus ne sont pas des mines -> on les met à 0
    for i in range (n):
        for j in range (m):
            if clues[i][j] != -1 :
                contraintes.append(x[i][j] == 0)
    
    # pour toutes les cases avec un indice dessus, 
    # on doit faire la somme de ses voisines (mais en excluant celles qui ne nous intéressent pas)
    # et cette somme doit valoir l'indice!
    for i in range (n):
        for j in range (m):
            if clues[i][j] != -1:
                voisins = voisinsValides(i,j,n,m)
                somme = Sum([x[a][b] for (a,b) in voisins])
                # attention, mieux de ne pas utiliser une somme ordinaire sur les contraintes (+=)
                contraintes.append(somme == clues[i][j])

    # il faut satisfaire toutes les contraintes
    satisfy(contraintes)


    if solve(solver=CHOCO) is SAT:
        # Si le solver a trouvé qlq chose de satisfiable, retourner les coordonnées des mines
        vals = values(x) # fonction de pycsp3 qui extrait les valeurs concrètes assignées par le solveur
        # pas oublier, x[i][j] n'est jamais vraiment une matrice qui contient des valeurs concrètes
        mines = []
        for i in range (n):
            for j in range (m):
                if vals[i][j] == 1:
                    mines.append((i,j))
        return mines
    else:
        return None

"""
La fonction retourne une liste qui contient les indices des voisins valables d'une case.
La case elle-même n'est pas inclue dans la liste et pas non plus les voisins qui n'existent pas (bords de la matrice)
"""
def voisinsValides(i: int, j: int, n: int, m: int):
    voisins = []
    for a in [-1,0,1]:
        for b in [-1,0,1]:
            if (((a,b)!=(0,0)) 
                and (i+a>=0) and (i+a <n) 
                and (j+b>=0) and (j+b <m)):
                voisins.append((i+a,j+b))
    return voisins


def check_solution(clues: list[list[int]], solution: list[(int, int)]) -> bool:
    n = len(clues)
    m = len(clues[0])
    mines_count = [[0 for _ in range(m)] for _ in range(n)]
    for x, y in solution:
        if clues[x][y] != -1:
            print(f"A mine is placed on a clue at position ({x},{y}), invalid solution")
            return False

        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if 0 <= x+a < n and 0 <= y + b < m and (a != 0 or b != 0):
                    mines_count[x + a][y + b] += 1

    for i in range(n):
        for j in range(m):
            if mines_count[i][j] != clues[i][j] and clues[i][j] != -1:
                print(f"The clue at position ({i},{j}) is not respected: there is {mines_count[i][j]} mines instead of {clues[i][j]}")
                return False

    return True


def parse_instance(input_file: str) -> list[list[int]]:
    with open(input_file) as input:
        lines = input.readlines()
    clues = []
    for line in lines:
        row = []
        for cell in line.strip().split(" "):
            row.append(int(cell))
        clues.append(row)
    return clues


if __name__ == '__main__':
    clues_list = ["instances/sat/i01.txt",
                  "instances/sat/i02.txt",
                  "instances/sat/i03.txt",
                  "instances/sat/i04.txt",
                  "instances/sat/i05.txt",
                  "instances/unsat/i01.txt",
                  "instances/unsat/i02.txt",
                  "instances/unsat/i03.txt",
                  "instances/unsat/i04.txt",
                  "instances/unsat/i05.txt"]
    for file_name in clues_list:
        clues = parse_instance(file_name)
        solution = solve_minesweeper(clues)
        if solution is not None:
            if check_solution(clues, solution):
                print("The returned solution is valid")
            else:
                print("The returned solution is not valid")
        else:
            print("No solution found")
