from BLL.Model.Queue import Queue
from BLL.Model.Task import Task


def processQueue(queue: Queue):
    for task in range(queue.rear):
            print(queue.items[task].name)
            print(queue.items[task].time)


task1 = Task("Task 1", 5, 1)
queue = Queue(10)
queue.enqueue(task1)
processQueue(queue)
