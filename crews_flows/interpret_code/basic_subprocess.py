import subprocess

result = subprocess.run(
    # ["ls", "-l"],
    # stdout=subprocess.PIPE,
    # stderr=subprocess.PIPE,
    # "ls -l",
    "python basic_exec.py",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
print(result.stdout)
print(result.stderr)

popen_result = subprocess.Popen(
    "python basic_exec.py",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

stdout, stderr = popen_result.communicate()
print(stdout)
print(stderr)
