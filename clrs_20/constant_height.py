class ConstantHeight:
    """A class to represent a constant height binary tree with a fixed universe size."""

    def __init__(self, u):
        self.u = u  # Universe size
        self.a = [0] * (u)  # Initialize vector a with zeros
        self.tree_size = 2 * u - 1  # Full binary tree size
        self.leaf_start = u - 1  # Start index for leaves in the binary tree
        self.tree = [0] * self.tree_size  # Initialize the binary tree
