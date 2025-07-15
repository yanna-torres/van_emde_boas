import random


class HashEntry:
    """
    Represents an entry in the hash table.\n
    Contains a key, a value, and a flag indicating if the entry is deleted.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.deleted = False


LARGE_PRIME = 2**31 - 1


class HashTable:
    """A hash table implementation with open addressing and linear probing.\n
    It supports dynamic resizing based on the load factor.\n
    The hash function is based on a linear combination of the key and two random integers `a` and `b`.\n
    The table resizes when the load factor exceeds 0.75 or drops below 0.25 and the capacity is greater than 4.
    The initial capacity is set to 4, and it can grow or shrink dynamically.\n
    The hash function uses a large prime number to reduce collisions.\n
    The `insert`, `get`, and `delete` methods allow for adding, retrieving, and removing entries.\n
    """

    def __init__(self, initial_capacity=4, a=None, b=None):
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

        self.p = LARGE_PRIME
        self.a = a if a is not None else random.randint(1, self.p - 1)
        self.b = b if b is not None else random.randint(0, self.p - 1)

    def _hash(self, key, i):
        """Computes the hash index for a given key and probe index `i`.\n
        The hash function is based on a linear combination of the key and two random integers `a` and `b`.\n
        It ensures that the index is within the bounds of the table's capacity.
        """
        base_hash = ((self.a * key + self.b) % self.p) % self.capacity
        return (base_hash + i) % self.capacity

    def _probe(self, key):
        """
        Finds the index for inserting or retrieving a key using linear probing.\n
        It checks for the first available slot or the slot containing the key.\n
        """
        for i in range(self.capacity):
            idx = self._hash(key, i)
            entry = self.table[idx]
            if entry is None or entry.key == key:
                return idx
        raise RuntimeError("Hash table is full")

    def _direct_insert(self, key, value):
        """
        Inserts a key-value pair directly into the hash table without probing.\n
        It uses the `_hash` function to find the index and inserts the entry.\n
        If the index is occupied, it raises an error indicating that the hash table is full.
        """
        for i in range(self.capacity):
            idx = self._hash(key, i)
            entry = self.table[idx]
            if entry is None or entry.deleted:
                self.table[idx] = HashEntry(key, value)
                self.size += 1
                return
            elif entry.key == key:
                self.table[idx].value = value
                return
        raise RuntimeError("Hash table is full during direct insert")

    def _resize(self, new_capacity):
        """
        Resizes the hash table to a new capacity.\n
        It rehashes all existing entries and reinserts them into the new table.\n
        The new capacity must be greater than 0.
        """
        old_table = self.table
        old_a = self.a
        old_b = self.b

        self.capacity = new_capacity
        self.table = [None] * self.capacity
        self.size = 0
        self.a = old_a
        self.b = old_b

        for entry in old_table:
            if entry and not entry.deleted:
                self._direct_insert(entry.key, entry.value)

    def _check_resize(self):
        """
        Checks the load factor of the hash table and resizes it if necessary.\n
        If the load factor exceeds 0.75, it doubles the capacity.\n
        If the load factor drops below 0.25 and the capacity is greater than 4, it halves the capacity.\n
        The load factor is calculated as the ratio of the number of entries to the capacity.
        """
        load = self.size / self.capacity
        if load > 0.75:
            self._resize(self.capacity * 2)
        elif load < 0.25 and self.capacity > 4:
            self._resize(self.capacity // 2)

    def insert(self, key, value):
        idx = self._probe(key)
        entry = self.table[idx]
        if entry is None or entry.deleted:
            self.table[idx] = HashEntry(key, value)
            self.size += 1
        else:
            self.table[idx].value = value
        self._check_resize()

    def get(self, key):
        for i in range(self.capacity):
            idx = self._hash(key, i)
            entry = self.table[idx]
            if entry is None:
                return None
            if not entry.deleted and entry.key == key:
                return entry.value
        return None

    def delete(self, key):
        for i in range(self.capacity):
            idx = self._hash(key, i)
            entry = self.table[idx]
            if entry is None:
                return
            if not entry.deleted and entry.key == key:
                entry.deleted = True
                self.size -= 1
                self._check_resize()
                return
