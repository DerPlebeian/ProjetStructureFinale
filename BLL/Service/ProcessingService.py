import time
import numpy as np
from scipy.stats import expon
from BLL.Model.Entities import Queue, ArrayStack, Task


def process(distribution):
    # [KPI 1] Define an array to get every poisson value
    total_intervals = []

    # [KPI 2] Define an array to collect every task times
    total_times = []

    # [KPI 4] Set a base value for the highest number of times in queue
    queue_highestnb = 0

    # Assign a Poisson value for each task
    for item in distribution:
        item.poisson = get_poisson(len(distribution))
        # Add that poisson value to the array previously defined
        total_intervals.append(item.poisson)
        give_exponential(item)
        total_times.append(item.time_frame)
        print(item.__str__())

    # Define a queue variable
    queue = Queue(10)

    # Define a waiting stack
    waiting: Queue = Queue(10)

    current_task = None

    for i in range(1):
        # Print the current loop iteration.
        print("\nIteration " + str(i))

        # Check if a task needs to be added to the queue
        for item in distribution:
            if item.poisson == i:
                queue.enqueue(item)
                check_queue_highestnb(queue, queue_highestnb)

        # Check if task added in higher priority than the current task
        if current_task is not None:
            if not waiting.is_empty():
                current_task = waiting.dequeue()
                print("Current task from waiting stack. " + current_task.__str__())

            if queue.peak().priority > current_task.priority:
                waiting.enqueue(current_task)
                current_task = queue.dequeue()
                print("Current task added because of superior priority. " + current_task.__str__())
        else:
            if not waiting.is_empty():
                current_task = waiting.dequeue()
                print("Current task from waiting stack. " + current_task.__str__())
            else:
                current_task = queue.dequeue()
                print("Current task from queue. " + current_task.__str__())

        # Print the queue
        # print("QUEUE: " + str(len(queue)) + " items")
        # print(queue.__str__())
        # Print how many are in waiting_stack
        # print("WAITING: " + str(len(waiting)) + " items")

        # Check if the current task is done processing
        if current_task is not None:
            # If not, add this iteration
            if (current_task.time_frame - current_task.time_executed) > 0:
                current_task.time_executed += 1
            # If so, dequeue it and remove it as the current task
            else:
                print("Current task is done. " + current_task.__str__())
                current_task = queue.dequeue()

        # For each iteration, sleep for one second
        time.sleep(1)

    # Print all the KPIs
    print("Key Performance Indicators: ")

    # KPI 1 - Get the average interval
    average_intervals = round(sum(total_intervals) / len(total_intervals))
    print("[KPI 1] Average interval: " + str(average_intervals))

    # KPI 2 - Get the average task time frame
    average_times = sum(total_times) / len(total_times)
    print("[KPI 2] Average task time frame: " + str(average_times))

    # KPI 5 - Get the probability of waiting
    waiting_probability = expon.cdf(x=1000, scale=999)
    print("[KPI 5] Probability of waiting: " + str(waiting_probability))

    # KPI 3 = everytime a current task is added, check with method for eveyry other item in queue +1 their queue wating time attribute

    # KPI 4 = in method to check poisson, check number of items in queue and gest highest of al time


def get_poisson(size):
    return np.random.poisson(size)


def give_exponential(task: Task):
    value = expon.rvs(scale=10, size=1)
    task.time_frame = value.item().__round__()
    return task


def check_queue_highestnb(queue, highestnb):
    if (len(queue)) > highestnb:
        highestnb = len(queue)


def main():
    distribution = [
        Task(101, 5, 1),
        Task(102, 3, 5),
        Task(103, 4, 3),
        Task(104, 2, 9)]

    process(distribution)


main()
