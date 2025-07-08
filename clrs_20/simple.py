class WithBTree:
    """Storing a dynamic set of integers in the range [0, u) using a vector and a binary tree."""

    def __init__(self, u):
        self.u = u  # Universe size
        self.a = [0] * (u)  # Initialize vector a with zeros

        # Binary tree that includes internal nodes + leaves from a
        self.tree_size = 2 * u - 1  # Full binary tree size
        self.tree = [0] * self.tree_size  # Initialize tree with zeros
        self.leaf_start = self.tree_size - u  # Start index of leaves in the tree
        self._rebuild_tree()

    def __str__(self):
        return f"WithBTree(u={self.u}, a={self.a}, tree={self.tree})"

    def _rebuild_tree(self):
        """Rebuilds the binary tree based on the current state of `a`."""
        # Sync leaves with a
        for i in range(self.u):
            self.tree[self.leaf_start + i] = self.a[i]
        # Build internal nodes using OR aggregation
        for i in reversed(range(self.leaf_start)):
            left = 2 * i + 1
            right = 2 * i + 2
            left_val = self.tree[left] if left < self.tree_size else 0
            right_val = self.tree[right] if right < self.tree_size else 0
            self.tree[i] = 1 if (left_val == 1 or right_val == 1) else 0

    def _update_tree_up(self, leaf_index):
        """Updates the binary tree upwards from the given leaf index."""
        i = self.leaf_start + leaf_index
        while i > 0:
            parent = (i - 1) // 2
            left = 2 * parent + 1
            right = 2 * parent + 2
            left_val = self.tree[left] if left < self.tree_size else 0
            right_val = self.tree[right] if right < self.tree_size else 0
            self.tree[parent] = 1 if (left_val == 1 or right_val == 1) else 0
            i = parent

    def insert(self, x):
        """Inserts an integer x into the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        self.a[x] = 1
        self.tree[self.leaf_start + x] = 1
        self._update_tree_up(x)

    def delete(self, x):
        """Deletes an integer x from the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        self.a[x] = 0
        self.tree[self.leaf_start + x] = 0
        self._update_tree_up(x)

    def member(self, x):
        """Checks if an integer x is a member of the set."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u:
            raise ValueError("x must be in the range [0, u)")
        return self.a[x] == 1

    def root_value(self):
        """Returns the value of the root of the binary tree."""
        return self.tree[0]

    def minimum(self):
        """Finds the minimum element in the set. Returns None if the set is empty. Go down the leftmost path."""
        i = 0
        while i < self.leaf_start:
            left = 2 * i + 1
            right = 2 * i + 2
            if left < self.tree_size and self.tree[left] == 1:
                i = left
            elif right < self.tree_size and self.tree[right] == 1:
                i = right
            else:
                return None
        return i - self.leaf_start

    def maximum(self):
        """Finds the maximum element in the set. Returns None if the set is empty. Go down the rightmost path."""
        i = 0
        while i < self.leaf_start:
            right = 2 * i + 2
            if right < self.tree_size and self.tree[right] == 1:
                i = right
            else:
                left = 2 * i + 1
                if left < self.tree_size and self.tree[left] == 1:
                    i = left
                else:
                    return None
        return i - self.leaf_start

    def successor(self, x):
        """Finds the smallest element greater than x. Returns None if no such element exists. Starts from the item x and goes up the tree."""
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if x < 0 or x >= self.u - 1:
            return None

        i = self.leaf_start + x
        # Step 1: go up until we find a parent where we can go right
        while i > 0:
            parent = (i - 1) // 2
            left = 2 * parent + 1
            right = 2 * parent + 2
            if left == i and right < self.tree_size and self.tree[right] == 1:
                # Step 2: go down from the right sibling
                i = right
                while i < self.leaf_start:
                    l = 2 * i + 1
                    r = 2 * i + 2
                    if l < self.tree_size and self.tree[l] == 1:
                        i = l
                    elif r < self.tree_size and self.tree[r] == 1:
                        i = r
                    else:
                        return None  # broken tree state (shouldn't happen)
                return i - self.leaf_start
            i = parent
        return None  # no successor

    def predecessor(self, x):
        if x <= 0 or x >= self.u:
            return None

        i = self.leaf_start + x
        # Step 1: go up until we can go left
        while i > 0:
            parent = (i - 1) // 2
            left = 2 * parent + 1
            right = 2 * parent + 2
            if right == i and self.tree[left] == 1:
                # Step 2: go down from left sibling
                i = left
                while i < self.leaf_start:
                    r = 2 * i + 2
                    l = 2 * i + 1
                    if r < self.tree_size and self.tree[r] == 1:
                        i = r
                    elif l < self.tree_size and self.tree[l] == 1:
                        i = l
                    else:
                        return None  # shouldn't happen in valid tree
                return i - self.leaf_start
            i = parent
        return None
