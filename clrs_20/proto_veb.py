import math


class ProtovEB:
    """A recursive solution"""

    def __init__(self, u):
        # u should be 2^(2^k)
        self.u = u
        self.k = int(math.sqrt(self.u))
        self.is_base = self.u == 2  # if u is 2, then does not have a summary
        size = self.u if self.is_base else self.k
        self.summary = ProtovEB(self.k) if not self.is_base else None
        self.a = [0 if self.is_base else ProtovEB(self.k)] * size

    def __str__(self):
        return f"ProtovEB(u={self.u}, k={self.k}, a={self.a}, summary={self.summary})"

    def high(self, x):
        return math.floor(x / self.k)

    def low(self, x):
        return x % self.k

    def index(self, x, y):
        return (x * self.k) + y


if __name__ == "__main__":
    tree = ProtovEB(16)
    print(tree)
