import subprocess

result = subprocess.run(['docker', 'run', '--rm', '-v', './excample.py', 'python:3.9', 'python', '/scripts/script.py'], capture_output=True, text=True)
print(result.stdout)