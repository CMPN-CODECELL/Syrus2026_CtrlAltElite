import subprocess

def run_tests(service):

    if service == "python-service":
        path = "../shopstack-platform/python-service"

        result = subprocess.run(
            ["python", "-m", "pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            cwd=path
        )

        return result.stdout

    elif service == "node-service":
        path = "../shopstack-platform/node-service"

        result = subprocess.run(
            ["npm", "test"],
            capture_output=True,
            text=True,
            cwd=path
        )

        return result.stdout + result.stderr

    return "Unknown service"