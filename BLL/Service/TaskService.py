import sys
import time

from BLL.Model.Entities import Queue, Task


def processQueue(queue: Queue):
    for task in range(queue.rear):
        print("==========================================================")
        print("CURRENT TASK: '" + queue.items[task].name + "'")
        for i in range(queue.items[task].time_frame + 1):
            sys.stdout.write("\r" + "Remaining time: " + str(queue.items[task].time_frame + 1 -
                                                             queue.items[task].time_executed) + " secs.")
            sys.stdout.flush()
            time.sleep(i)
            queue.items[task].time_executed += 1
        sys.stdout.write("\r" + "Task execution is over (5 seconds).")
        print("\n==========================================================")


task1 = Task("Task 1", 5, 1)
queue = Queue(10)
queue.enqueue(task1)
processQueue(queue)
