import subprocess

result = subprocess.run(
    # ["ls", "-l"],
    # stdout=subprocess.PIPE,
    # stderr=subprocess.PIPE,
    # "ls -l",
    # "python basic_exec.py",
    "lt -l",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
# print("Stdout:", result.stdout)
# print("StdErr:", result.stderr)

popen_result = subprocess.Popen(
    "ls -l",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

stdout, stderr = popen_result.communicate()
print(stdout)
print(stderr)
