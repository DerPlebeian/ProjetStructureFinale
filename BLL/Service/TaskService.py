import sys
import time
import os
import random
clear = lambda: os.system('cls')

from BLL.Model.Entities import Queue, Task

queue = Queue(10)
queue.enqueue(Task(id=0, priority=(random.randint(1, 10)), time_frame=(random.randint(5, 10))))
currentTask: Task = queue.items[queue.rear]
waiting_stack = []


runningTask: Task = queue.items[queue.rear]
while runningTask.id == currentTask.id:
    if newTask.priority > currentTask.priority:
        waiting_stack += currentTask
        currentTask = newTask

    print("\r" + "CURRENT TASK: '" + str(currentTask.id) + "'")
    for i in range(currentTask.time_frame + 1):
        sys.stdout.write("\r" + "Remaining time: " + str(queue.items[task].time_frame + 1 -
                                                         queue.items[task].time_executed) + " secs.")
        time.sleep(i)
        queue.items[task].time_executed += 1


def main(queue, distribution):
    for i in range(30):
        time.sleep(random.randint(1, 3))
        queue.enqueue(Task(id=i+1, priority=(random.randint(1, 10)), time_frame=(random.randint(5, 10))))


queue = Queue(10)
queue.items = [Task(101, 10, 1)]
main(Queue(), [1, 3, 5, 7])
