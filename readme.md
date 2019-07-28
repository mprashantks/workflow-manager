# Workflow Manager!
Your very own workflow manager.

## Docs

1. **CreateWorkflow.py** contains a predefined user input as received from UI. This input is used to create workflow with all the provided tasks. After creation of workflow object, processes for each task are started. These processes takes input from relevant task-input queue, computes the result and feed it to relevant task-output queues.
2. **Workflow.py** contains class declaration for workflow.
3. **Task.py** contains class declaration for all available tasks.
4. **test_producer.py** produces input for workflow for testing.
5. **test_workflow_output.py** reads workflow output from queue.
6. **test_workflow_fault.py** reads workflow fault if any from queue.


## Dependencies
RabbitMQ

## How to use
Run files in given below order:
1. **test_workflow_output.py**
2. **test_workflow_fault.py**
3. **CreateWorkflow.py**
4. **test_producer.py**

## What's remaining
1. Using **ray** in place of python's **Multiprocessing Pool** to run processes on cluster of computers.
2. Running RabbitMQ on a standalone server for communication with all computers in distributed environment.