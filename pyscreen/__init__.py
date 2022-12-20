__all__ = ['Screen', 'create', 'kill', 'exists', 'ls']

import os, signal
import subprocess
from datetime import datetime
from pyscreen.errors import *

class Screen:
    def __init__(self, pid):
        """
        :param pid: The process ID of the screen
        Creates a new Screen object
        """
        if not exists(pid):
            raise ScreenNotFound(f"No screen with pid {pid}")
        self.pid = pid

    def self_destruct(self):
        kill(self.pid)

    def send(self, command: str, end="\r") -> None:
        """
        :param command: The command to be run
        :param end: Appended to the end of the command - the default value is a carriage return
        """
        os.system(f'screen -S {self.pid} -X stuff {command}{end}')

def create(name, shell=os.environ['SHELL'], logfile=None, title=None) -> Screen:
    command = ["screen", "-DmS", name, '-s', shell]
    if logfile:
        command.append('-Logfile')
        command.append(logfile)
    if title:
        command.append('-t')
        command.append(title)
    process = subprocess.Popen(command)
    return Screen(process.pid)

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
        final[pid]['time'] = datetime.strptime(item[1], '%m/%d/%Y %X %p')
    return final


