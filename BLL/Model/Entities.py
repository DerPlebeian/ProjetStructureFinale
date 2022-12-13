import ctypes


class Queue:

    # Constructor
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.front = 0
        self.rear = 0
        self.items = [0 for i in range(capacity)]

    # Put an item in a queue
    def enqueue(self, item):
        if self.capacity == self.rear:
            print("Queue is full")
            return
        self.items[self.rear] = item
        self.rear += 1

    # Removes an item from the queue and returns it
    def dequeue(self):
        if self.is_empty():
            print("Queue is empty")
            return
        to_return = self.items[self.front]
        self.shift_left(self.front)
        self.rear -= 1
        return to_return

    # Go an index to the left in the queue
    def shift_left(self, index):
        for i in range(index, self.rear - 1):
            self.items[i] = self.items[i + 1]

    # Returns if the queue is empty
    def is_empty(self):
        if self.front == self.rear == 0:
            return True
        return False

    def __len__(self):
        return self.rear

    # Check first item in queue
    def peak(self):
        return self.items[self.front]

    def __str__(self):
        to_return = "["
        for i in range(self.rear):
            to_return = to_return + str(self.items[i])
            if i < self.rear - 1:
                to_return = to_return + "," + "\n"
        return to_return + "]"

    @staticmethod
    def build_array(capacity):
        return (capacity * ctypes.py_object)()


class Task:
    def __init__(self, id, time_frame, priority):
        self.id = id
        self.time_frame = time_frame
        self.time_executed = 0
        self.priority = priority
        self.poisson = 0

    def __str__(self):
        to_return = \
            "[ID: " + str(self.id) + \
            ", Priority:" + str(self.priority) + \
            ", Time: " + str(self.time_executed) + "/" + str(self.time_frame) + \
            ", Poisson: " + str(self.poisson)
        return to_return + "]"
