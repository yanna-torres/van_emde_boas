import math
from hash_table import HashTable


class RSVanEmdeBoas:
    """
    RSVanEmdeBoas is a van Emde Boas tree implementation using a hash table for clusters to reduce the space used.\n
    It supports operations like insert, delete, member, minimum, maximum, successor, and predecessor.\n
    It is designed for integers in the range `[0, u-1]`.\n
    The tree is structured with a summary for clusters and uses a hash table to manage clusters.\n
    The base case is when `u = 2`, where it behaves like a simple bit vector.
    The tree supports efficient operations with `O(log log u)` time complexity for most operations.
    """

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

        cluster_outputs = []
        for i in range(self.clusters.capacity):
            entry = self.clusters.table[i]
            if entry and not entry.deleted:
                cluster_index = entry.key
                cluster = entry.value
                values = cluster.__reconstruct_values__()
                if values:
                    full_values = [self.index(cluster_index, v) for v in values]
                    full_values_str = ", ".join(
                        str(v) for v in sorted(set(full_values))
                    )
                    cluster_outputs.append(f"C[{cluster_index}]: {full_values_str}")

        output.extend(cluster_outputs)
        return ", ".join(output)

    def __reconstruct_values__(self):
        """
        Reconstructs the values stored in the van Emde Boas tree.\n
        Returns a list of integers representing the values in the tree.\n
        This method is used for visualization purposes.
        """
        if self.min is None:
            return []

        values = []
        values.append(self.min)

        if self.max is not None and self.max != self.min:
            values.append(self.max)

        if not self.is_base:
            for i in range(self.clusters.capacity):
                entry = self.clusters.table[i]
                if entry and not entry.deleted:
                    cluster_index = entry.key
                    cluster = entry.value
                    cluster_values = cluster.__reconstruct_values__()
                    for val in cluster_values:
                        full_val = self.index(cluster_index, val)
                        if full_val not in values:
                            values.append(full_val)

        return values

    def high(self, x):
        """
        Returns the high part of the integer `x` in the van Emde Boas tree.\n
        The high part is the integer division of `x` by the lower square root of `u`.
        """
        return x // self.lower_sqrt

    def low(self, x):
        """
        Returns the low part of the integer `x` in the van Emde Boas tree.\n
        The low part is the remainder of `x` when divided by the lower square root of `u`.
        """
        return x % self.lower_sqrt

    def index(self, x, y):
        """
        Combines the high part `x` and low part `y` into a single integer.\n
        The result is calculated as `x * lower_sqrt + y`, where `lower_sqrt` is the lower square root of `u`.
        """
        return x * self.lower_sqrt + y

    def minimum(self):
        """
        Returns the minimum value in the van Emde Boas tree.\n
        If the tree is empty, it returns `None`.
        """
        return self.min

    def maximum(self):
        """
        Returns the maximum value in the van Emde Boas tree.\n
        If the tree is empty, it returns `None`.
        """
        return self.max

    def member(self, x):
        """
        Checks if the integer `x` is a member of the van Emde Boas tree.\n
        Returns `True` if `x` is in the tree, otherwise returns `False`.
        If `x` is equal to the minimum or maximum, it returns `True` directly.\n
        If the tree is a base case, it returns `False`, given that it only contains 0 and 1.\n
        For non-base cases, it checks the cluster corresponding to the high part of `x`.
        """
        if x == self.min or x == self.max:
            return True
        if self.is_base:
            return False
        cluster = self.clusters.get(self.high(x))
        return cluster.member(self.low(x)) if cluster else False

    def successor(self, x):
        """
        Returns the successor of the integer `x` in the van Emde Boas tree.\n
        If `x` is less than the minimum, it returns the minimum.\n
        If `x` is greater than the maximum, it returns `None`.\n
        For non-base cases, it checks the cluster corresponding to the high part of `x`.
        """
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
        """
        Returns the predecessor of the integer `x` in the van Emde Boas tree.\n
        If `x` is greater than the maximum, it returns the maximum.\n
        If `x` is less than the minimum, it returns `None`.\n
        For non-base cases, it checks the cluster corresponding to the high part of `x`.
        """
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
        """
        Inserts the integer `x` into the van Emde Boas tree.\n
        If the tree is empty, it sets both minimum and maximum to `x`.\n
        If `x` is less than the current minimum, it swaps them.\n
        For non-base cases, it calculates the high and low parts of `x` and inserts.
        If the cluster for the high part does not exist, it creates a new cluster.\n
        If the cluster is empty, it updates the summary to include the high part.
        """
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
        """
        Deletes the integer `x` from the van Emde Boas tree.\n
        If the tree becomes empty, it sets both minimum and maximum to `None`.\n
        If `x` is the minimum, it updates the minimum to the next successor.\n
        For non-base cases, it finds the appropriate cluster and deletes the element.
        If the cluster becomes empty, it removes it from the clusters and updates the summary.
        """
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
