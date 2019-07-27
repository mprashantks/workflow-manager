import time


class TaskBase:
    id = None
    name = None
    description = None
    parallel_limit = None
    time_limit = None
    input = None
    output = None

    def __init__(self, id, name, description, parallel_limit, time_limit):
        self.id = id
        self.name = name
        self.description = description
        self.parallel_limit = parallel_limit
        self.time_limit = time_limit
        self.input = None
        self.output = []


class TaskAdd(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=10,
            time_limit=2
        )

    def perform_operation(self):
        print('{} implementation'.format(self.name))


class TaskSubtract(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=6,
            time_limit=10
        )

    def perform_operation(self):
        print('{} implementation'.format(self.name))


class TaskProduct(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=2,
            time_limit=15
        )

    def perform_operation(self):
        print('{} implementation'.format(self.name))


class TaskDivision(TaskBase):
    def __init__(self, id, name, description):
        super().__init__(
            id=id,
            name=name,
            description=description,
            parallel_limit=3,
            time_limit=4
        )

    def perform_operation(self):
        print('{} implementation'.format(self.name))
