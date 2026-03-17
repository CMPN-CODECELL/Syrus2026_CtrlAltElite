import os
import shutil
import tempfile

def create_sandbox(file_path):
    sandbox_dir = tempfile.mkdtemp()

    try:
        sandbox_file = os.path.join(sandbox_dir, os.path.basename(file_path))
        shutil.copy(file_path, sandbox_file)
        return sandbox_dir, sandbox_file
    except:
        return None, None


def apply_patch(file_path, patch_code):
    try:
        with open(file_path, "a", encoding="utf8") as f:
            f.write("\n\n# === PATCH APPLIED ===\n")
            f.write(patch_code)

        return True
    except:
        return False


def run_tests_simulation():
    return {
        "test_cases": 3,
        "passed": 3,
        "failed": 0,
        "status": "All tests passed"
    }


def generate_patch_log(file_path, patch):
    return f"""
PATCH LOG
-------------------------
File Modified: {file_path}

Changes Applied:
{patch}

Status: SUCCESS
"""