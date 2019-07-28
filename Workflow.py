from Task import *
from constants import *


class Workflow:
    def __init__(self, name):
        self.id = int(time.time())
        self.name = name
        self.input = 'wf.{}.in'.format(self.name)
        self.num_output = 0
        self.output = []
        self.tasks = dict()
        self.processed_tasks = set()
        self.parallel_limit = 0

    @staticmethod
    def _get_connected_tasks(task, task_relationship):
        '''
        Get connected tasks

        :param task: (int) task ID
        :param task_relationship: (dict) Relationships b/w tasks received from UI
        :return: (list) Connected tasks
        '''
        t = task_relationship.get(task)
        if t is not None:
            return t
        return []

    def _is_task_processed(self, task):
        '''
        Check if task has already been processed

        :param task: (int) task ID
        :return: (Boolean) Task visited or not
        '''
        return task in self.processed_tasks

    def _create_task(self, task, task_input, task_info):
        '''
        Create task object

        :param task: (int) task ID
        :param task_input: (str) RabbitMQ queue used for reading inputs
        :param task_info: (dict) Task information received from UI
        :return: (Task Object) Relevant task object
        '''
        task_name = task_info.get(task).get('name')

        if task_name == ADD:
            task_obj = TaskAdd(
                id=task,
                name=task_info.get(task).get('user_provided_name'),
                description=task_info.get(task).get('user_provided_desc')
            )
        elif task_name == SUBTRACT:
            task_obj = TaskSubtract(
                id=task,
                name=task_info.get(task).get('user_provided_name'),
                description=task_info.get(task).get('user_provided_desc')
            )
        elif task_name == PRODUCT:
            task_obj = TaskProduct(
                id=task,
                name=task_info.get(task).get('user_provided_name'),
                description=task_info.get(task).get('user_provided_desc')
            )
        elif task_name == DIVISION:
            task_obj = TaskDivision(
                id=task,
                name=task_info.get(task).get('user_provided_name'),
                description=task_info.get(task).get('user_provided_desc')
            )
        else:
            raise ValueError('Incorrect task name', task_name)

        task_obj.input = task_input
        self.processed_tasks.add(task)
        self.parallel_limit += task_obj.parallel_limit
        return task_obj

    def _create_relationships(self, task, task_input, task_relationship, task_info):
        '''
        Performs DFS traversal while creating and storing tasks and their relationships

        :param task: (int) current task ID
        :param task_input: (str) RabbitMQ queue used for reading inputs
        :param task_relationship: (dict) Relationships b/w tasks received from UI
        :param task_info: (dict) Task information received from UI
        :return:
        '''
        try:
            task_obj = self._create_task(task=task, task_input=task_input, task_info=task_info)
            connected_tasks = self._get_connected_tasks(task=task, task_relationship=task_relationship)

            for index, connected_task in enumerate(connected_tasks):
                if self._is_task_processed(task=connected_task):
                    # Take already existing queue
                    task_obj.output.append(self.tasks.get(connected_task).input)
                else:
                    task_obj_output = 'tk.{0}.out.{1}'.format(task_obj.id, index + 1)
                    task_obj.output.append(task_obj_output)
                    self._create_relationships(
                        task=connected_task,
                        task_input=task_obj_output,
                        task_relationship=task_relationship,
                        task_info=task_info
                    )

            if not task_obj.output:
                task_obj_output = 'wf.{0}.out.{1}'.format(self.name, self.num_output+1)
                task_obj.output.append(task_obj_output)
                self.output.append(task_obj_output)
                self.num_output += 1
            self.tasks[task_obj.id] = task_obj

        except ValueError as err:
            print(err.args)

        except Exception as err:
            print(err.args)

    def create_workflow(self, user_input):
        '''
        Create workflow with all tasks

        :param user_input: (dict) received from UI
        :return:
        '''
        self._create_relationships(
            task=user_input.get('start_task'),
            task_input=self.input,
            task_relationship=user_input.get('task_relationship'),
            task_info=user_input.get('task_info')
        )
