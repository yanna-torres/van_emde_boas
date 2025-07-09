import math


class ConstantHeight:
    """A class to represent a constant height binary tree with a fixed universe size."""

    def __init__(self, u):
        if not (u > 0 and (u & (u - 1)) == 0):
            raise ValueError("u must be a power of 2")
        self.u = u  # Universe size
        self.a = [0] * (u)  # Initialize vector a with zeros

        # k is the square root of the universe size - amount of clusters
        self.k = int(math.sqrt(u))
        self.summary = [0] * (self.k)

    def __str__(self):
        return f"ConstantHeight(u={self.u}, k={self.k}, a={self.a}, summary={self.summary})"

    def insert(self, x):
        """Inserts an integer x into the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        self.a[x] = 1
        index_summary = math.floor(x / self.k)
        self.summary[index_summary] = 1

    def delete(self, x):
        """Deletes an integer x from the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        self.a[x] = 0
        index_summary = math.floor(x / self.k)
        # Check if all elements in the cluster containing x are 0
        cluster_start = index_summary * self.k
        cluster_end = (index_summary + 1) * self.k
        if all(val == 0 for val in self.a[cluster_start:cluster_end]):
            self.summary[index_summary] = 0

    def member(self, x):
        """Checks if an integer x is a member of the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        return self.a[x] == 1

    def minimum(self):
        """Finds the minimum element in the set."""
        cluster_index = self.summary.index(1) if 1 in self.summary else -1
        if cluster_index == -1:
            return None
        cluster_start = cluster_index * self.k
        for i in range(cluster_start, cluster_start + self.k):
            if self.a[i] == 1:
                return i

    def maximum(self):
        """Finds the maximum element in the set."""
        cluster_reversed_index = (
            self.summary[::-1].index(1) if 1 in self.summary else -1
        )
        cluster_index = len(self.summary) - 1 - cluster_reversed_index
        if cluster_index == -1:
            return None
        cluster_start = cluster_index * self.k
        for i in range(cluster_start + self.k - 1, cluster_start - 1, -1):
            if self.a[i] == 1:
                return i

    def predecessor(self, x):
        """Finds the predecessor of x in the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        current_cluster_index = math.floor(x / self.k)
        current_cluster_start = current_cluster_index * self.k
        current_cluster_end = (current_cluster_index + 1) * self.k
        # Search in the current cluster
        for i in range(current_cluster_end - 1, current_cluster_start - 1, -1):
            if self.a[i] == 1 and i < x:
                return i
        # If we find a 1, return the largest index less than x
        if current_cluster_index == 0:
            return None
        # Search in the previous clusters
        summary_pivot = self.summary[:current_cluster_index]
        previous_cluster_reversed_index = (
            summary_pivot[::-1].index(1) if 1 in summary_pivot else -1
        )
        previous_cluster_index = (
            len(summary_pivot) - 1 - previous_cluster_reversed_index
        )
        if previous_cluster_index == -1:
            return None
        previous_cluster_start = previous_cluster_index * self.k
        previous_cluster_end = (previous_cluster_index + 1) * self.k
        for i in range(previous_cluster_end - 1, previous_cluster_start - 1, -1):
            if self.a[i] == 1 and i < x:
                return i
            
    def successor(self, x):
        """Finds the successor of x in the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        current_cluster_index = math.floor(x / self.k)
        current_cluster_start = current_cluster_index * self.k
        current_cluster_end = (current_cluster_index + 1) * self.k
        # Search in the current cluster
        for i in range(current_cluster_start, current_cluster_end):
            if self.a[i] == 1 and i > x:
                return i
        # If we find a 1, return the smallest index greater than x
        if current_cluster_index == len(self.summary) - 1:
            return None
        # Search in the next clusters
        summary_pivot = self.summary[current_cluster_index + 1 :]
        next_cluster_index = summary_pivot.index(1) if 1 in summary_pivot else -1
        if next_cluster_index == -1:
            return None
        next_cluster_start = (current_cluster_index + 1 + next_cluster_index) * self.k
        for i in range(next_cluster_start, next_cluster_start + self.k):
            if self.a[i] == 1 and i > x:
                return i


if __name__ == "__main__":
    u = 2**4
    tree = ConstantHeight(u)

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
    print(tree)
    print("Minimum:", tree.minimum())
    print("Maximum:", tree.maximum())
    print("Predecessor of 5:", tree.predecessor(5))
    print("Predecessor of 14:", tree.predecessor(14))
    print("Predecessor of 7:", tree.predecessor(7))
    print("Successor of 5:", tree.successor(5))
    print("Successor of 14:", tree.successor(14))
