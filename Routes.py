from typing import List
from Address import Address
from Maps import get_distance_in_seconds


def compute_distance_graph(addresses: List[Address]):
    n = len(addresses)
    distance_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            frm = addresses[i].to_address_str()
            to = addresses[j].to_address_str()
            dist = get_distance_in_seconds(frm, to)
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist

    return distance_matrix


class Unionfind:
    def __init__(self, vertices: int):
        self.v = vertices
        self.parent = [i for i in range(vertices)]
        self.rank = [0 for _ in range(vertices)]

    def find(self, i: int):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, u, v):
        if self.rank[u] < self.rank[v]:
            self.parent[u] = v
        elif self.rank[u] > self.rank[v]:
            self.parent[v] = u
        else:
            self.parent[v] = u
            self.rank[u] += 1


def compute_optimal_route(addresses: List[Address], distance_matrix: List[List[int]]):
    n = len(addresses)
    unionfind = Unionfind(n)
    edges, res = [], []
    for i in range(n):
        for j in range(n):
            edges.append((i, j, distance_matrix[i][j]))
    edges = sorted(edges, key=lambda item: item[2])
    i, e = 0, 0
    while e < n-1:
        u, v, w = edges[i]
        i += 1
        x = unionfind.find(u)
        y = unionfind.find(v)

        if x != y:
            e += 1
            res.append((u, v, w))
            unionfind.union(x, y)
