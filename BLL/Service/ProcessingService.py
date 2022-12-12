import time

import numpy as np
from BLL.Model.Entities import Queue, ArrayStack, Task


def process(distribution):
    # Assign a Poisson value for each task
    for item in distribution:
        item.poisson = get_poisson(len(distribution))
        print(item.__str__())

    # Define a queue variable
    queue = Queue(10)

    # Define a waiting stack
    waiting: Queue = Queue(10)

    current_task = None

    for i in range(1000):
        # Print the current loop iteration.
        print("\nIteration " + str(i))

        # Select a task in the queue. It is the one being processed.
        #if not queue.is_empty():
        #    current_task: Task = queue.items[queue.front]
        #    print("Current task - " + str(current_task.id))
        #else:
        #    current_task: Task = None
        ###

        # Check if a task needs to be added to the queue
        for item in distribution:
            if item.poisson == i:
                queue.enqueue(item)

                # Check if task added in higher priority than the current task
                if current_task is not None:
                    if item.priority > current_task.priority:
                        waiting.enqueue(current_task)
                        current_task = item
                    else:
                        queue.enqueue(item)
                else:
                    current_task = item


        # Print the queue
        print("QUEUE: " + str(len(queue)) + " items")
        print(queue.__str__())

        # Print how many are in waiting_stack
        print("WAITING: " + str(len(waiting)) + " items")

        # Check if the current task is done processing
        if current_task is not None:
            # If not, add this iteration
            if (current_task.time_frame - current_task.time_executed) > 0:
                current_task.time_executed += 1
            # If so, dequeue it and remove it as the current task
            else:
                queue.dequeue()

        # Check is the queue is empty and that the waiting stack isn't empty
        if queue.is_empty():
            if not waiting.is_empty():
                # If both are checked, enqueue an item from the waiting stack
                queue.enqueue(waiting.items[waiting.front])
                queue.dequeue()

        # For each iteration, sleep for one second
        time.sleep(1)


def get_poisson(size):
    return np.random.poisson(size)


def main():
    distribution = [
        Task(101, 5, 1),
        Task(102, 3, 5),
        Task(103, 4, 3),
        Task(104, 2, 9)]

    process(distribution)


main()
