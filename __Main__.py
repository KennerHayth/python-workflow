import sys
import os

# base folder for all referenced scripts
current_dir = os.path.dirname(__file__)
automation_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(automation_dir)

# all scripts to be used in the workflow
from RPA_Import import Daily_RPA_FLPA_Import

from FACTS4DEMES import facts4demes

from FLPA_Export import Daily_FLPA_Exports

from GP_Export import Daily_GP_Export

from ONM_Export import ONM_SC


class function:
    def __init__(self,name,dependencies,status)
    self.name = self.name
    self.dependencies = self.dependencies
    self.status = self.status

    def updateStatus(self,new_status):
        if new_status == "Failed"
            self.status = new_status
            print(f"{self.name} has marked as failed")
        if new_status == "Passed"
            self.status = new_status
            print(f"{self.name} has marked as Passed")


RPA_Import = function(name="rpa_import", dependencies =[], status = "pending")
    