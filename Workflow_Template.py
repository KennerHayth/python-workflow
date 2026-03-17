import sys
import os
import subprocess
import time
from enum import Enum, auto


# Base folder for all referenced scripts is found to allow for clean relative import references
current_dir = os.path.dirname(__file__)
automation_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(automation_dir)

# List of task
task_list = []

# Class of all Status states
class TaskState(Enum):
    PENDING = auto()
    RUNNING = auto()
    PASSED = auto()
    FAILED = auto()


# Use this class to define a new script process within the workflow
class Function:
    def __init__(self,name,dependencies,script):
        self.name = name
        self.dependencies = dependencies
        self.status = TaskState.PENDING
        self.script = script
        self.processor = None

# Is the script ready to run? how about its dependencies?
    def can_run(self):
        for dep in self.dependencies:
            if dep.status == TaskState.PENDING or dep.status == TaskState.RUNNING:
                print(rf"{self.name} the dependency {dep.name} is not ready")
                return False
            if dep.status == TaskState.FAILED:
                self.status = TaskState.FAILED
                print(rf"{self.name} can not run. {dep.name} has failed")   
                return False
        print(f"dependencies for {self.name} are all complete.")
        return True

# Run the script. double checks that it starts as pending
    def start(self):
        print("attempting start")
        if self.status != TaskState.PENDING:
            return
        self.processor = subprocess.Popen([sys.executable, self.script])
        print("process attempted")
        self.status = TaskState.RUNNING
        print(f"{self.name} has started")

# Update what the status of the running process is 
    def update(self):
        if self.status != TaskState.RUNNING:
            return
        process_status = self.processor.poll()
        if process_status is None:
            # this process is still running
            return
        elif process_status == 0:
            self.status = TaskState.PASSED
        else:
            self.status = TaskState.FAILED
            print(f"{self.name} has failed")

# When defining a "Function" provide a string, list of dependencies (any other defined "Function"), a script using (importname).__file__ or a file path


# ── EXAMPLE USAGE ──────────────────────────────────────────────
# Replace the imports and Function definitions below with your own scripts.
# Each script should be importable and have a .__file__ attribute or be directly called using their file path.

# from task_1 import task_a
# task_a_class = Function(name="task_a", dependencies =[], script = task_a.__file__)
# # append task to the list of task
# task_list.append(task_a_class)

# from task_2 import task_b
# task_b_class = Function(name="task_b", dependencies =[task_a_class], script = task_b.__file__)
# task_list.append(task_b_class)

# ───────────────────────────────────────────────────────────────



# Tracking task, uses a dictonary to relate a running process to a task
current_task= {}
# Number of task allowed to run at one time
MAX_TASK = 5

# Main processed used to handle the entire workflow using the features provided by the class
def run_workflow(task_list):
    while any(t.status in [TaskState.PENDING, TaskState.RUNNING] for t in task_list):
        
        
        for task in list(task_list):
            if task.status == TaskState.PENDING and task.can_run():
                if len(current_task) < MAX_TASK:
                    task.start()
                    current_task[task] = task.processor

        finished = []
        for task in current_task:
            task.update()
            if task.status != TaskState.RUNNING:
                finished.append(task)
    
        for task in finished:
            del current_task[task]
    
        time.sleep(1)

run_workflow(task_list)
