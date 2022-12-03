class Task:
    def __init__(self, name, time_frame, priority):
        self.name = name
        self.time_frame = time_frame
        self.time_executed = 0
        self.priority = priority
