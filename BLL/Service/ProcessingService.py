import time
import numpy as np
from scipy.stats import expon
from BLL.Model.Entities import Queue, Task


def process(distribution):
    # Dictionary to know how much time task took in the CPU
    dictionary = {}

    # [KPI 1] Define an array to get every poisson value
    total_intervals = []

    # [KPI 2] Define an array to collect every task times
    total_times = []

    # [KPI 4] Set a base value for the highest number of times in queue
    queue_highestnb = 0

    # Define a variable to receive the highest poisson value in the distribution
    highest_poisson = 0

    # Assign a Poisson value for each task
    for item in distribution:
        item.poisson = get_poisson(len(distribution))
        if item.poisson > highest_poisson:
            highest_poisson = item.poisson
        # Add that poisson value to the array previously defined
        total_intervals.append(item.poisson)
        give_exponential(item)
        total_times.append(item.time_frame)
        print(item.__str__())

    # Define a queue variable
    queue = Queue(10)

    # Define a waiting stack
    waiting: Queue = Queue(10)

    current_task: Task = None

    for iteration in range(120):
        # Print the current loop iteration.
        print("\nIteration " + str(iteration))

        # Check if a task needs to be added to the queue
        for item in distribution:
            # If the poisson of the task equals the iteration, enqueue the item in the main queue
            if item.poisson == iteration:
                queue.enqueue(item)
                # KPI 4
                queue_highestnb = check_queue_highestnb(queue, queue_highestnb)

        # Check if task added in higher priority than the current task
        if current_task is not None:
            if not queue.is_empty():
                if queue.peak().id != current_task.id:
                    if queue.peak().priority > current_task.priority:
                        waiting.enqueue(current_task)
                        current_task = queue.dequeue()
                        queued_waiting_times(queue)
                        print("Current task (priority): " + current_task.__str__())

            if current_task is not None:
                if not waiting.is_empty():
                    if queue.peak().id != current_task.id:
                        if waiting.peak().priority > current_task.priority:
                            waiting.enqueue(current_task)
                            current_task = waiting.dequeue()
                            queued_waiting_times(queue)
                            print("Current task (from waiting stack): " + current_task.__str__())
            else:
                if not waiting.is_empty():
                    waiting.enqueue(current_task)
                    current_task = waiting.dequeue()
                    queued_waiting_times(queue)
                    print("Current task (from waiting stack): " + current_task.__str__())

        else:
            # If there is a task in the waiting queue, put it back in the main queue
            if not waiting.is_empty():
                current_task = waiting.dequeue()
                queued_waiting_times(queue)
                print("Current task (from waiting stack): " + current_task.__str__())
            else:
                current_task = queue.dequeue()
                queued_waiting_times(queue)
                print("Current task (from queue): " + current_task.__str__())

        # Check if the current task is done processing
        if current_task is not None:
            # If not, add this iteration
            if (current_task.time_frame - current_task.time_executed) > 0:
                current_task.time_executed += 1
            # If so, dequeue it and remove it as the current task
            else:
                print('\033[1m' + "Current task is done. " + '\033[0m' + current_task.__str__())
                queued_waiting_times(queue)
                dictionary[current_task.id] = iteration  # Add the time in dictionary
                current_task = queue.dequeue()

        # For each iteration, sleep for one second
        time.sleep(1)

    # Dictionary - See times
    print("\n==================================================================")
    print('\033[1m' + "Task Dictionary: " + '\033[0m')
    print(dictionary)

    # Print all the KPIs
    print("==================================================================")
    print('\033[1m' + "Key Performance Indicators: " + '\033[0m')

    # KPI 1 - Get the average interval
    average_intervals = round(sum(total_intervals) / len(total_intervals))
    print("[KPI 1] Average interval: " + str(average_intervals))

    # KPI 2 - Get the average task time frame
    average_times = sum(total_times) / len(total_times)
    print("[KPI 2] Average task time frame: " + str(average_times))

    # KPI 3 = Get the average queue waiting time
    average_waiting_array = []
    for task in distribution:
        average_waiting_array.append(task.queue_waiting_time)
    average_waiting = sum(average_waiting_array) / len(average_waiting_array)
    print("[KPI 3] Average queue waiting time: " + str(average_waiting) + " seconds")

    # KPI 4 - The highest number of items in queue
    print("[KPI 4] Highest number of items in queue: " + str(queue_highestnb))

    # KPI 5 - Get the probability of waiting
    waiting_probability = expon.cdf(x=120, scale=10)
    print("[KPI 5] Probability of waiting: " + (str(waiting_probability * 100)) + "%")
    print("==================================================================\n")


# Gives the poisson value to a task using a poisson formula
def get_poisson(size):
    return np.random.poisson(size)


# Gives the time to a task using an exponential formula
def give_exponential(task: Task):
    value = expon.rvs(scale=10, size=1)
    task.time_frame = value.item().__round__()
    return task


# Checks the maximum tasks that were in the main queue
def check_queue_highestnb(queue, highestnb):
    if len(queue) > highestnb:
        highestnb = len(queue)
    return highestnb


# Checks how long the tasks were queued
def queued_waiting_times(queue):
    if not queue.is_empty():
        for i in range(len(queue)):
            queue.items[i].queue_waiting_time += 1
