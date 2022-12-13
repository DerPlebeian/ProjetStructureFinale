import random

from BLL.Model.Entities import *
from BLL.Service.ProcessingService import process


def main():
    distribution = []
    task_qty = random.randint(5, 20)

    for x in range(task_qty):
        distribution.append(Task(priority=random.randint(1, 10)))

    process(distribution)


main()
