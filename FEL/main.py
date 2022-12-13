from BLL.Model.Entities import *
from BLL.Service.ProcessingService import process


def main():
    distribution = [
        Task(101, 5, 1),
        Task(102, 3, 5),
        Task(103, 4, 3),
        Task(104, 2, 9)]

    process(distribution)


main()
