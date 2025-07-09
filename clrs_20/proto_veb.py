import math


class ProtovEB:
    """A recursive solution"""

    def __init__(self, u):
        # u should be 2^(2^k)
        self.u = u  # universe size
        self.k = int(math.sqrt(self.u))  # quantity of clusters
        self.is_base = self.u == 2  # if u is 2, then does not have a summary
        size = self.u if self.is_base else self.k
        self.summary = ProtovEB(self.k) if not self.is_base else None
        if self.is_base:
            self.a = [0] * size
        else:
            self.a = [ProtovEB(self.k) for _ in range(size)]

    def __str__(self):
        return f"ProtovEB(u={self.u}, k={self.k}, a={self.__reconstruct_vector__()}, summary={self.summary.__reconstruct_vector__() if self.summary else None})"

    def __reconstruct_vector__(self):
        if self.u == 2:
            return self.a
        result = []
        for i, cluster in enumerate(self.a):
            cluster_values = cluster.__reconstruct_vector__()
            for j, val in enumerate(cluster_values):
                result.append(val)
        return result

    def high(self, x):
        return math.floor(x / self.k)

    def low(self, x):
        return x % self.k

    def index(self, x, y):
        return (x * self.k) + y


if __name__ == "__main__":
    tree = ProtovEB(16)
    print(tree)
