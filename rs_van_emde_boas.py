import math
from hash_table import HashTable


class RSVanEmdeBoas:
    def __init__(self, u):
        self.u = u
        self.is_base = u == 2
        log_u = int(math.log2(u))
        self.upper_sqrt = 2 ** math.ceil(log_u / 2)
        self.lower_sqrt = 2 ** math.floor(log_u / 2)
        self.min = None
        self.max = None
        self.summary = None
        self.clusters = HashTable()

    def __str__(self):
        output = []
        if self.min is None:
            output.append("Min: None")
            return " ".join(output)

        output.append(f"Min: {self.min}")

        # Reconstrói os dados armazenados agrupados por cluster
        cluster_outputs = []
        for i in range(self.clusters.capacity):
            entry = self.clusters.table[i]
            if entry and not entry.deleted:
                cluster_index = entry.key
                cluster = entry.value
                values = cluster.__reconstruct_values__()
                if values:
                    full_values = [cluster.index(cluster_index, v) for v in values]
                    full_values_str = ", ".join(
                        str(v) for v in sorted(set(full_values))
                    )
                    cluster_outputs.append(f"C[{cluster_index}]: {full_values_str}")

        output.extend(cluster_outputs)
        return ", ".join(output)

    def __reconstruct_values__(self):
        values = []
        if self.min is not None:
            values.append(self.min)
            if self.max != self.min:
                values.append(self.max)

        if not self.is_base:
            for i in range(self.clusters.capacity):
                entry = self.clusters.table[i]
                if entry and not entry.deleted:
                    cluster = entry.value
                    cluster_vals = cluster.__reconstruct_values__()
                    values.extend(cluster_vals)

        return values

    def high(self, x):
        return x // self.lower_sqrt

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
        cluster = self.clusters.get(self.high(x))
        return cluster.member(self.low(x)) if cluster else False

    def successor(self, x):
        if self.is_base:
            if x == 0 and self.max == 1:
                return 1
            return None
        if self.min is not None and x < self.min:
            return self.min

        high = self.high(x)
        low = self.low(x)
        cluster = self.clusters.get(high)
        if cluster and low < cluster.maximum():
            offset = cluster.successor(low)
            return self.index(high, offset)

        if self.summary is None:
            return None
        succ_cluster = self.summary.successor(high)
        if succ_cluster is None:
            return None
        offset = self.clusters.get(succ_cluster).minimum()
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
        cluster = self.clusters.get(high)
        if cluster and low > cluster.minimum():
            offset = cluster.predecessor(low)
            return self.index(high, offset)

        if self.summary is None:
            if self.min is not None and x > self.min:
                return self.min
            return None

        pred_cluster = self.summary.predecessor(high)
        if pred_cluster is None:
            if self.min is not None and x > self.min:
                return self.min
            return None
        offset = self.clusters.get(pred_cluster).maximum()
        return self.index(pred_cluster, offset)

    def insert(self, x):
        if self.min is None:
            self.min = x
            self.max = x
            return

        if x < self.min:
            x, self.min = self.min, x

        if not self.is_base:
            high = self.high(x)
            low = self.low(x)
            cluster = self.clusters.get(high)

            if cluster is None:
                cluster = RSVanEmdeBoas(self.lower_sqrt)
                self.clusters.insert(high, cluster)

            if cluster.minimum() is None:
                if self.summary is None:
                    self.summary = RSVanEmdeBoas(self.upper_sqrt)
                self.summary.insert(high)
                cluster.min = low
                cluster.max = low
            else:
                cluster.insert(low)

        if x > self.max:
            self.max = x

    def delete(self, x):
        if self.min == self.max:
            self.min = None
            self.max = None
            return

        if self.is_base:
            self.min = 1 - x
            self.max = self.min
            return

        if x == self.min:
            if self.summary is None:
                self.min = self.max
                return
            first_cluster = self.summary.minimum()
            x = self.index(first_cluster, self.clusters.get(first_cluster).minimum())
            self.min = x

        high = self.high(x)
        low = self.low(x)
        cluster = self.clusters.get(high)

        if cluster:
            cluster.delete(low)
            if cluster.minimum() is None:
                self.clusters.delete(high)
                if self.summary:
                    self.summary.delete(high)
                    if self.summary.minimum() is None:
                        self.summary = None

                if x == self.max:
                    summary_max = self.summary.maximum() if self.summary else None
                    if summary_max is None:
                        self.max = self.min
                    else:
                        self.max = self.index(
                            summary_max, self.clusters.get(summary_max).maximum()
                        )
            elif x == self.max:
                self.max = self.index(high, cluster.maximum())


if __name__ == "__main__":
    tree = RSVanEmdeBoas(16)
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
