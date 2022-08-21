from subprocess import PIPE, STDOUT, Popen
from threading import Timer
from typing import List

from software_privacy.logger import Logger


def run_command(
    cmd: List[str], timeout: int = None, stdout_logger: Logger = None
) -> int:
    """Perform secure system calls.

    Args:
        cmd (List[str]): The command to perform and its arguments
        timeout (int, optional): Timeout for command, in seconds
        stdout_logger (Logger, optional): Prints each returned line to this function. STDERR is piped to STDOUT.
    Returns:
        (int): Return code
    """

    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    timer = Timer(timeout, proc.kill)
    stdout_logger(f"START system call: {cmd}...")
    try:
        timer.start()
        for stdout_line in iter(proc.stdout.readline, ""):
            if stdout_line:
                stdout_logger(stdout_line)
    finally:
        timer.cancel()
    stdout_logger(f"END system call: {cmd}.")
    return proc.returncode
