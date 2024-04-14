__all__ = ['Screen', 'create', 'kill', 'exists', 'ls']

import os, signal
import subprocess
from datetime import datetime
from pyscreen.errors import *

class Screen:
    def __init__(self, pid, close_on_del=False):
        """
        :param pid: The process ID of the screen
        Creates a new Screen object
        """
        if not exists(pid):
            raise ScreenNotFound(f"No screen with pid {pid}")
        self.pid = pid
        self.close_on_del=close_on_del

    def __del__(self):  # Destroy screen process when object deleted
        if self.close_on_del:
            kill(self.pid)

    def send(self, command: str, end="\r") -> None:
        """
        :param command: The command to be run
        :param end: Appended to the end of the command - the default value is a carriage return
        """
        os.system(f'screen -S {self.pid} -X stuff {command}{end}')
    
    def enable_logging(self):
        """
        Enables logging to a temporary file
        """
        os.system(f'screen -S {self.pid} -X logfile /tmp/pyscreen-{self.pid}.log')
    
    def get_log(self, readlines=False):
        with open(f'/tmp/pyscreen-{self.pid}.log', 'r') as log_file:
            if readlines:
                return log_file.readlines()
            else:
                log_text = log_file.read()
        with open(f'/tmp/pyscreen-{self.pid}.log', 'w') as log_file:
            log_file.write('')
            log_file.truncate()
        return log_text
        


def create(name, shell=os.environ['SHELL'], logfile=None, title=None, close_on_del=True) -> Screen:
    command = ["screen", "-DmS", name, '-s', shell]
    if logfile:
        command.append('-Logfile')
        command.append(logfile)
    if title:
        command.append('-t')
        command.append(title)
    process = subprocess.Popen(command)
    while not process.pid: pass
    return Screen(process.pid, close_on_del=close_on_del)

def kill(pid):
    os.kill(pid, signal.SIGTERM)

def exists(pid: int) -> int:
    command = f"screen -S {str(pid)} -Q select .".split()
    pop = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    pop.wait()
    code = pop.returncode
    return False if code else True

def ls() -> dict:
    out = subprocess.check_output(["screen", "-ls"]).decode()
    out = out.replace('\t', '')
    out = out.split('\n')
    out = out[1:len(out)-2]
    out = [i.replace(")", "").split("(") for i in out]
    final = {}
    for item in out:
        process = item[0].split('.')
        pid = process[0]
        final[pid] = {'name': process[1]}  # final: {pid:{...}, ... }
        # final[pid]['time'] = datetime.strptime(item[1], '%m/%d/%Y %X %p')  # This will break on some systems
    
    return final
