import heapq
from collections import deque, defaultdict


def f_null(x):
    return x


class PriorityQueue:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order='min', f=f_null):
        self.heap_set = set()

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
        self.heap_set.add(item)

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            item = heapq.heappop(self.heap)[1]
            self.heap_set.remove(item)
            return item
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

    def __contains__(self, value):
        """Return True if the value is in PriorityQueue."""
        return value in self.heap_set

    def __getitem__(self, value):
        """Returns the first key associated with  in PriorityQueue.
        Raises KeyError if key is not present."""
        for key, item in self.heap:
            if item == value:
                return key
        raise KeyError(str(value) + " is not in the priority queue")

    def __delitem__(self, value):
        """Delete the first occurrence of value."""
        try:
            self.heap_set.remove(value)
            del self.heap[[item == value for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(value) + " is not in the priority queue")
        heapq.heapify(self.heap)

    def __repr__(self, simple=True):
        if simple:
            return str([key for key, value in self.heap])
        return f"Priority Queue at: {id(self)} [f{self.f} heap:{self.heap}]"


class PriorityQueueImproved:
    """A Queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first.
    If order is 'min', the item with minimum f(x) is
    returned first; if order is 'max', then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    MOCK_MAX = 9999

    def __init__(self, order='min', f=f_null):
        self.min = self.MOCK_MAX
        self.key_to_values = defaultdict(set)
        self.value_to_key = {}

        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("order must be either 'min' or 'max'.")

    def append(self, value):
        """insert item at its correct position."""
        key = self.f(value)
        if value in self.value_to_key:
            self.update(key, value)

        if key < self.min:
            self.min = key
        # First mapping
        self.key_to_values[key].add(value)
        # Second mapping
        self.value_to_key[value] = key

    def extend(self, items):
        """insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """pop and return the item (with min or max f(x) value)
        depending on the order."""
        # If not empty
        if self.key_to_values:
            # find and pop the least cost
            items = self.key_to_values[self.min]
            item = items.pop()
            # find the next min if the current list exhausted
            if not len(items):
                del self.key_to_values[self.min]
                # move it to the new min
                self.min += 1
                while self.min not in self.key_to_values:
                    self.min += 1
            # Remove from node_to_cost
            del self.value_to_key[item]

            return item
        else:
            raise Exception('trying to pop from empty PriorityQueue.')

    def _remove_from_key_to_values(self, key, value):
        if key in self.key_to_values and value in self.key_to_values[key]:
            # Remove from key to value
            values = self.key_to_values[key]
            values.remove(value)

            # Update min if needed
            if not len(values):
                del self.key_to_values[key]
                # If the dictionary is not empty yet
                if key == self.min and len(self.key_to_values):
                    self.min += 1
                    while self.min not in self.key_to_values:
                        self.min += 1
                elif not len(self.key_to_values):
                    self.min = self.MOCK_MAX
        else:
            raise Exception

    def update(self, new_key, value):
        assert value in self.value_to_key
        old_key = self.value_to_key[value]
        if new_key == old_key:
            return
        self.value_to_key[value] = new_key
        if new_key < self.min:
            self.min = new_key
        self.key_to_values[new_key].add(value)
        self._remove_from_key_to_values(old_key, value)

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.key_to_values)

    def __contains__(self, value):
        """Return True if the value is in PriorityQueue."""
        return value in self.value_to_key

    def __getitem__(self, value):
        """
        Find based on item
        This is possible only because the state created by state will be
        the same if they have the same dictionary

        Returns the first key associated with value in PriorityQueue."""
        assert value in self.value_to_key
        return self.value_to_key[value]

    def __delitem__(self, value):
        """Delete the first occurrence of value."""
        try:
            key = self.value_to_key[value]
            del self.value_to_key[value]

            self._remove_from_key_to_values(key, value)
        except ValueError:
            raise KeyError(str(value) + " is not in the priority queue")

    def __repr__(self):
        return f"Priority Queue at: {id(self)} [f{self.f}" \
            f"heap:{self.key_to_values}]"


if __name__ == "__main__":
    elements = [1, 2, 3, 4, 5, 6, 7, 1, 3, 4, 43, 3, 42345, 6253, 23451,
                1, 23, 423, 4]

    # q = PriorityQueue()
    # q.extend(elements)
    # print(q)
    # q.update(100, 1)
    # print(q)
    # q.update(0, 42345)
    # print(q)

    q2 = PriorityQueueImproved()
    q2.extend(elements)
    print(q2.key_to_values, q2.value_to_key)

    q2.update(2, 1)
    print(q2.key_to_values, q2.value_to_key)

    print(q2.pop())
