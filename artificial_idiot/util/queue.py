import heapq


def f_null(x):
    return x


class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=f_null):
        self.heap = []

        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, [self.f(item), item])

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def find(self, item):
        # Simply use a linear search
        for pos, pair in enumerate(self.heap):
            if pair[1] == item:
                return pos, pair
        return -1, None

    def update(self, new_key, item):
        # Find then update
        pos, pair = self.find(item)
        assert pair is not None and pos is not -1
        # Update the key
        old_key = pair[0]
        pair[0] = new_key

        # update the position
        # NOTE: Python's Fking implementation reverses sift up and down.
        if new_key < old_key:
            heapq._siftdown(self.heap, 0, pos)
        else:
            heapq._siftup(self.heap, pos)

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

    def __repr__(self):
        return f"Priority Queue at {id(self)}:\nf={self.f}\n{self.heap}"


if __name__ == "__main__":
    elements = [1, 2, 3, 4, 5, 6, 7, 1, 3, 4, 43, 3, 42345, 6253, 23451,
                1, 23, 423, 4]

    q = PriorityQueue()
    q.extend(elements)
    print(q)
    q.update(100, 1)
    print(q)
    q.update(0, 42345)
    print(q)
