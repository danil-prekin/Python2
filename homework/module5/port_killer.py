import os
import signal
import subprocess
import time
import shlex

def run_server_on_port(port):
    def is_port_in_use(port):
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        return result.returncode == 0

    def kill_process_on_port(port):
        result = subprocess.run(['lsof', '-t', '-i', f':{port}'], capture_output=True, text=True)
        pids = result.stdout.strip().split()
        for pid in pids:
            if pid:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass

    while is_port_in_use(port):
        kill_process_on_port(port)
        time.sleep(1)

    cmd = shlex.split(f'python3 -m http.server {port}')
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc
