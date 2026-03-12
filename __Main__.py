import sys
import os
import subprocess
import time


# base folder for all referenced scripts
current_dir = os.path.dirname(__file__)
automation_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(automation_dir)

# all scripts to be used in the workflow
# from FACTS4DEMES import facts4demes

# from GP_Export import Daily_GP_Export

# from ONM_Export import ONM_SC


workweek_task = []
# weekend_task = []

# use this class to define a new function
class Function:
    def __init__(self,name,dependencies,script):
        self.name = name
        self.dependencies = dependencies
        self.status = "Pending"
        self.script = script

    def updateStatus(self,new_status):
        if new_status == "Failed":
            self.status = new_status
            print(f"{self.name} has marked as Failed")
        elif new_status == "Passed":
            self.status = new_status
            print(f"{self.name} has marked as Passed")
        else: 
            self.status = "Error"
            print("invalid status selected")

    def check_deps(self):
        for dep in self.dependencies:
            if dep.status == "Pending":
                print(f"{self.name} has been skipped for pending {dep.name}")
                return False
            if dep.status == "Failed" or dep.status == "Error":
                self.updateStatus("Failed")
                return False

        return True

# when defining a function provide a string, list of dependancies (any other defined "Function"), a script using importname.__file__ or a file path

from RPA_Import import Daily_RPA_FLPA_Import
RPA_Import = Function(name="rpa_import", dependencies =[], script = Daily_RPA_FLPA_Import.__file__)
# append task to the list of task
workweek_task.append(RPA_Import)

from FLPA_Export import Daily_FLPA_Exports
FLPA_Export = Function(name="flpa_export", dependencies =[RPA_Import], script = Daily_FLPA_Exports.__file__)
workweek_task.append(FLPA_Export)


# tracking task, uses a dictonary to relate a running process to a task
current_task= {}
# Number of task allowed to run at one time
MAX_TASK = 5

# main processed used to handle the entire workflow
def run_task():
    # if there are any task that are waiting or task that are running: keep looping
    while len(workweek_task) > 0 or len(current_task) > 0:
        finished_task =[]

        # for task in a COPY of the list of task.
        for task in list(workweek_task):
            # remove any task that has been marked Pass/Fail/Error and move on
            if task.status != "Pending":
                workweek_task.remove(task)
                continue
            # have the dependancies completed? True/False
            task_ready = task.check_deps()

            # if task_ready is True and there is less than 5 task running, start task.
            if task_ready and len(current_task) < MAX_TASK:
                process = subprocess.Popen([sys.executable,task.script])
                current_task[task] = process
                workweek_task.remove(task)
        
        #check in on all current running task and get their current status
        for task,process in current_task.items():
            status_check = process.poll()
            if status_check is not None:
                if status_check == 0:
                    task.updateStatus("Passed")
                elif status_check != 0:
                    task.updateStatus("Failed")
                
                finished_task.append(task)

        # close out any task that were marked complete in previous section
        for task in finished_task:
            del current_task[task]

        time.sleep(1)

run_task()