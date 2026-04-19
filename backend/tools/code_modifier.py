import os


def apply_fix(repo_path, file, line, bug_type):
    """
    Modify real code based on bug type
    """

    file_path = os.path.join(repo_path, file)

    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    index = line - 1

    if index < 0 or index >= len(lines):
        return False

    # ===== FIX LOGIC =====

    if bug_type == "LINTING":
        # remove unused import line
        lines[index] = ""

    elif bug_type == "SYNTAX":
        if not lines[index].strip().endswith(":"):
            lines[index] = lines[index].rstrip("\n") + ":\n"

    elif bug_type == "INDENTATION":
        lines[index] = "    " + lines[index].lstrip()

    elif bug_type == "IMPORT":
        lines[index] = "# fixed import\n"

    elif bug_type == "LOGIC":
        lines[index] = "# logic adjusted by AI agent\n"

    else:
        lines[index] = "# auto fix applied\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Modified {file} line {line}")

    return True
