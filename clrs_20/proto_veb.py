import math


class ProtovEB:
    """A recursive solution"""

    def __init__(self, u):
        # u should be 2^(2^k)
        self.u = u  # universe size
        self.k = int(math.sqrt(self.u))  # quantity of clusters
        self.n = 0  # number of elements in the set
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

    def member(self, x):
        if self.is_base:
            return self.a[x] == 1
        high = self.high(x)
        low = self.low(x)
        return self.a[high].member(low)

    def minimum(self):
        if self.is_base:
            if self.a[0] == 1:
                return 0
            elif self.a[1] == 1:
                return 1
            return None
        min_cluster = self.summary.minimum()
        if min_cluster is None:
            return None
        offset = self.a[min_cluster].minimum()
        return self.index(min_cluster, offset)

    def maximum(self):
        if self.is_base:
            if self.a[1] == 1:
                return 1
            elif self.a[0] == 1:
                return 0
            return None
        max_cluster = self.summary.maximum()
        if max_cluster is None:
            return None
        offset = self.a[max_cluster].maximum()
        return self.index(max_cluster, offset)

    def successor(self, x):
        if self.is_base:
            if x == 0 and self.a[1] == 1:
                return 1
            return None
        offset = self.a[self.high(x)].successor(self.low(x))
        if offset is not None:
            return self.index(self.high(x), offset)
        succ_cluster = self.summary.successor(self.high(x))
        if succ_cluster is None:
            return None
        offset = self.a[succ_cluster].minimum()
        return self.index(succ_cluster, offset)

    def predecessor(self, x):
        if self.is_base:
            if x == 1 and self.a[0] == 1:
                return 0
            return None
        offset = self.a[self.high(x)].predecessor(self.low(x))
        if offset is not None:
            return self.index(self.high(x), offset)
        pred_cluster = self.summary.predecessor(self.high(x))
        if pred_cluster is None:
            return None
        offset = self.a[pred_cluster].maximum()
        return self.index(pred_cluster, offset)

    def insert(self, x):
        if self.is_base:
            self.a[x] = 1
            self.n += 1
            return
        high = self.high(x)
        low = self.low(x)
        if not self.a[high].member(low):
            self.a[high].insert(low)
            if self.summary is not None:
                self.summary.insert(high)
            self.n += 1
        else:
            return

    def delete(self, x):
        if self.is_base:
            self.a[x] = 0
            self.n = max(0, self.n - 1)
            if self.n == 0:
                self.summary = None
            return
        high = self.high(x)
        low = self.low(x)
        if self.a[high].member(low):
            self.a[high].delete(low)
            if not self.a[high].minimum():
                self.summary.delete(high)
            self.n = max(0, self.n - 1)
        else:
            return


if __name__ == "__main__":
    tree = ProtovEB(16)
    print(tree)

    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)
    tree.insert(7)
    tree.insert(14)
    tree.insert(15)
    print(tree)

    tree.delete(2)
    print(tree)
    print("Member 3:", tree.member(3))
    tree.delete(3)
    print("Minimum:", tree.minimum())
    print("Maximum:", tree.maximum())
    print("Predecessor of 5:", tree.predecessor(5))
    print("Predecessor of 14:", tree.predecessor(14))
    print("Predecessor of 7:", tree.predecessor(7))
    print("Successor of 5:", tree.successor(5))
    print("Successor of 14:", tree.successor(14))
