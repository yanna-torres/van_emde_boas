import math


class VanEmdeBoas:
    def __init__(self, u):
        self.u = u  # universe size
        # if u is a even power of 2, k_upper and k_lower are equal
        self.k_upper = math.ceil(math.sqrt(u))  # upper bound of k
        self.k_lower = math.floor(math.sqrt(u))  # lower bound of k
        self.is_base = u == 2

        self.min = None  # minimum element, does not appear in the clusters
        self.max = None  # maximum element, appears in the clusters

        self.summary = None
        self.clusters = None
        if not self.is_base:
            self.summary = VanEmdeBoas(self.k_upper)  # exists only if u > 2
            self.clusters = [VanEmdeBoas(self.k_lower) for _ in range(self.k_upper)]

    def __str__(self):
        return f"VanEmdeBoas(u={self.u}, min={self.min}, max={self.max}, summary={self.summary}, data={self.clusters})"

    def high(self, x):
        return math.floor(x / self.k_lower)

    def low(self, x):
        return x % self.k_lower

    def index(self, x, y):
        return x * self.k_lower + y

    def minimum(self):
        return self.min

    def maximum(self):
        return self.max

    def member(self, x):
        if x == self.min or x == self.max:
            return True
        if self.is_base:
            return False
        high = self.high(x)
        low = self.low(x)
        return self.clusters[high].member(low)

    def sucessor(self, x):
        if self.is_base:
            if x == 0 and self.max == 1:
                return 1
            return None
        if self.min is not None and x < self.min:
            return self.min
        high = self.high(x)
        low = self.low(x)
        max_low = self.clusters[high].maximum()
        if max_low is not None and low < max_low:
            offset = self.clusters[high].sucessor(low)
            return self.index(high, offset)
        succ_cluster = self.summary.sucessor(high)
        if succ_cluster is None:
            return None
        offset = self.clusters[succ_cluster].minimum()
        return self.index(succ_cluster, offset)

    def predecessor(self, x):
        if self.is_base:
            if x == 1 and self.min == 0:
                return 0
            return None
        if self.max is not None and x > self.max:
            return self.max
        high = self.high(x)
        low = self.low(x)
        min_low = self.clusters[high].minimum()
        if min_low is not None and low > min_low:
            offset = self.clusters[high].predecessor(low)
            return self.index(high, offset)
        pred_cluster = self.summary.predecessor(high)
        if pred_cluster is None:
            if self.min is not None and x > self.min:
                return self.min
            return None
        offset = self.clusters[pred_cluster].maximum()
        return self.index(pred_cluster, offset)

    def empty_tree_insert(self, x):
        self.min = x
        self.max = x
        return

    def insert(self, x):
        if self.min is None:
            self.empty_tree_insert(x)
        if x < self.min:
            x, self.min = self.min, x  # exchange x with self.min
            if self.u > 2:
                high = self.high(x)
                low = self.low(x)
                if self.clusters[high].minimum() is None:
                    self.summary.insert(high)
                    self.clusters[high].empty_tree_insert(low)
                else:
                    self.clusters[high].insert(low)
        if x > self.max:
            self.max = x


if __name__ == "__main__":
    # Example usage
    tree = VanEmdeBoas(16)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)
    tree.insert(7)
    tree.insert(14)
    tree.insert(15)
    print(tree)
