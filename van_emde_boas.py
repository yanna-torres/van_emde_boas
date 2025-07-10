import math


class VanEmdeBoas:
    def __init__(self, u):
        self.u = u  # universe size
        self.is_base = u == 2

        # if u is 2^y, k_upper and k_lower are equal
        log_u = int(math.log2(u))
        self.upper_sqrt = 2 ** math.ceil(log_u / 2)
        self.lower_sqrt = 2 ** math.floor(log_u / 2)

        self.min = None  # minimum element, does not appear in the clusters
        self.max = None  # maximum element, appears in the clusters

        self.summary = None
        self.clusters = None
        if not self.is_base:
            self.summary = VanEmdeBoas(self.upper_sqrt)  # exists only if u > 2
            self.clusters = [
                VanEmdeBoas(self.lower_sqrt) for _ in range(self.upper_sqrt)
            ]

    def __str__(self):
        return f"VanEmdeBoas(u={self.u}, min={self.min}, max={self.max}, summary=(u={self.summary.u}, data={self.summary.__reconstruct_vector__()}), data={self.__reconstruct_vector__()})"

    def __reconstruct_vector__(self):
        if self.min is None:
            return []

        result = [self.min] if self.min == self.max else [self.min]

        if not self.is_base:
            for i in range(self.upper_sqrt):
                cluster = self.clusters[i]
                cluster_vals = cluster.__reconstruct_vector__()
                for val in cluster_vals:
                    result.append(self.index(i, val))

        if self.max != self.min:
            result.append(self.max)

        return sorted(set(result))

    def high(self, x):
        return math.floor(x / self.lower_sqrt)

    def low(self, x):
        return x % self.lower_sqrt

    def index(self, x, y):
        return x * self.lower_sqrt + y

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

    def successor(self, x):
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
            offset = self.clusters[high].successor(low)
            return self.index(high, offset)
        succ_cluster = self.summary.successor(high)
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
            return
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

    def delete(self, x):
        if self.min == self.max:
            self.min = None
            self.max = None
            return
        if self.is_base:
            if x == 0:
                self.min = 1
            else:
                self.min = 0
            self.max = self.min
            return
        if x == self.min:
            first_cluster = self.summary.minimum()
            x = self.index(first_cluster, self.clusters[first_cluster].minimum())
            self.min = x
        high = self.high(x)
        low = self.low(x)
        self.clusters[high].delete(low)
        if self.clusters[high].minimum() is None:
            self.summary.delete(high)
            if x == self.max:
                summary_max = self.summary.maximum()
                if summary_max is None:
                    self.max = self.min
                else:
                    self.max = self.index(
                        summary_max, self.clusters[summary_max].maximum()
                    )
        else:
            if x == self.max:
                self.max = self.index(high, self.clusters[high].maximum())


if __name__ == "__main__":
    # Example usage
    tree = VanEmdeBoas(32)
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
