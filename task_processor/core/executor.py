import subprocess
from typing import List
from task_runner.core.models import Task
from task_runner.utils.logging import LogManager


class TaskExecutor:
    def __init__(self, log_manager: LogManager):
        self.log_manager = log_manager

    def execute_task(self, task: Task) -> None:
        log_file = self.log_manager.get_log_file(task.name)

        try:
            # Split command into list for secure execution
            cmd = task.command.split()

            # Execute command and capture output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False,  # Prevent shell injection
            )

            stdout, stderr = process.communicate()

            # Log output
            with open(log_file, "a") as f:
                f.write(f"=== Task: {task.name} ===\n")
                f.write(f"Command: {task.command}\n")
                f.write(
                    f"Status: {'Success' if process.returncode == 0 else 'Failed'}\n"
                )
                f.write(f"Return Code: {process.returncode}\n")
                if stdout:
                    f.write("\n=== Output ===\n")
                    f.write(stdout)
                if stderr:
                    f.write("\n=== Error ===\n")
                    f.write(stderr)
                f.write("\n\n")

            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd)

        except Exception as e:
            # Log error
            with open(log_file, "a") as f:
                f.write(f"=== Task: {task.name} ===\n")
                f.write(f"Command: {task.command}\n")
                f.write(f"Status: Failed\n")
                f.write(f"Error: {str(e)}\n\n")
            raise
