#import atexit
import os
import sys

_, pid_path, stdout_path, stderr_path, *args = sys.argv

if os.fork() > 0:
    sys.exit(0)

os.chdir('/')
os.setsid()
os.umask(0)

if os.fork() > 0:
    sys.exit(0)

sys.stdout.flush()
sys.stderr.flush()
stdout = open(stdout_path, 'a+')
stderr = open(stderr_path, 'a+')
os.dup2(stdout.fileno(), sys.stdout.fileno())
os.dup2(stderr.fileno(), sys.stderr.fileno())

with open(pid_path, 'w') as f:
    print(os.getpid(), file=f)

os.execv(args[0], args)
