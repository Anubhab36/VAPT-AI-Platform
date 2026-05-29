
import subprocess

target = "scanme.nmap.org"

result = subprocess.run(
    ["nmap", target],
    capture_output=True,
    text=True
)

print("Target:", target)
print(result.stdout)