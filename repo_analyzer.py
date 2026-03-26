import os

def search_repo(keywords, base_path):

    matched_files = []

    for root, dirs, files in os.walk(base_path):

        for file in files:

            if file.endswith(".py") or file.endswith(".js") or file.endswith(".ts"):

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf8", errors="ignore") as f:

                        content = f.read().lower()

                        for keyword in keywords:
                            if keyword.lower() in content:
                                matched_files.append(file_path)
                                break

                except:
                    continue

    return matched_files