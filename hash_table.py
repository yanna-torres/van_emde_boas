import random


class HashEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.deleted = False


LARGE_PRIME = 2**31 - 1


class HashTable:
    def __init__(self, initial_capacity=4, a=None, b=None):
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

        self.p = LARGE_PRIME
        self.a = a if a is not None else random.randint(1, self.p - 1)
        self.b = b if b is not None else random.randint(0, self.p - 1)

    def _hash(self, key, i):
        base_hash = ((self.a * key + self.b) % self.p) % self.capacity
        return (base_hash + i) % self.capacity

    def _probe(self, key):
        for i in range(self.capacity):
            idx = self._hash(key, i)
            entry = self.table[idx]
            if entry is None or entry.key == key:
                return idx
        raise RuntimeError("Hash table is full")

    def _direct_insert(self, key, value):
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
