from Workflow import Workflow
import multiprocessing


def start_tasks(workflow):
    print('Workflow Input `{}`'.format(workflow.input))
    pool = multiprocessing.Pool(processes=workflow.parallel_limit)

    for task in workflow.tasks.values():
        for i in range(task.parallel_limit):
            pool.apply_async(task.consume)

    pool.close()
    pool.join()


if __name__ == '__main__':
    # User Input received from UI in form of JSON
    ui_input = {
        'task_info': {
            1: {'name': 'add', 'user_provided_name': 'Task A', 'user_provided_desc': 'Add two numbers'},
            2: {'name': 'product', 'user_provided_name': 'Task B', 'user_provided_desc': 'Multiply two numbers'},
            3: {'name': 'add', 'user_provided_name': 'Task C', 'user_provided_desc': 'Add numbers'},
            4: {'name': 'subtract', 'user_provided_name': 'Task D', 'user_provided_desc': 'Subtract numbers'},
            5: {'name': 'division', 'user_provided_name': 'Task E', 'user_provided_desc': 'Divide numbers'},
            6: {'name': 'product', 'user_provided_name': 'Task F', 'user_provided_desc': 'Multiply numbers'}
        },
        'task_relationship': {
            1: [{'con': None, 'out': 2}],
            2: [{'con': None, 'out': 3}, {'con': None, 'out': 4}],
            3: [{'con': None, 'out': 5}],
            4: [{'con': None, 'out': 5}],
            5: [{'con': '<', 'out': 6}]
        },
        # 'task_relationship': {
        #     1: [{'con': None, 'out': 2}],
        #     2: [{'con': None, 'out': 3}, {'con': None, 'out': 4}],
        #     3: [{'con': None, 'out': 5}],
        #     4: [{'con': None, 'out': 5}],
        #     5: [{'con': '>', 'out': 6}]
        # },
        'start_task': 1
    }

    workflow = Workflow(name='test')
    # Create workflow from provided input
    workflow.create_workflow(user_input=ui_input)

    # Start workflow tasks as separate processes
    start_tasks(workflow)

