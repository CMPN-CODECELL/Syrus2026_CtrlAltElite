import os
import re

REPO_PATH = "../shopstack-platform"


# ==============================
# STEP 1: BUILD INDEX
# ==============================
def build_index():

    index = []

    for root, dirs, files in os.walk(REPO_PATH):

        for file in files:

            if file.endswith((".js", ".ts", ".py")):

                file_path = os.path.join(root, file)

                # Detect file type
                path_lower = file_path.lower()

                if "controller" in path_lower:
                    file_type = "controller"
                elif "service" in path_lower:
                    file_type = "service"
                elif "route" in path_lower:
                    file_type = "api"
                else:
                    file_type = "other"

                functions = []
                apis = []

                try:
                    with open(file_path, "r", encoding="utf8", errors="ignore") as f:
                        content = f.read()

                        # ---------------------------
                        # FUNCTION EXTRACTION
                        # ---------------------------
                        functions = re.findall(r"def\s+\w+|function\s+\w+", content)

                        # ---------------------------
                        # API DETECTION
                        # ---------------------------
                        if "app.get" in content or "router.get" in content:
                            apis.append("GET API")

                        if "app.post" in content or "router.post" in content:
                            apis.append("POST API")

                        if "app.put" in content or "router.put" in content:
                            apis.append("PUT API")

                        if "app.delete" in content or "router.delete" in content:
                            apis.append("DELETE API")

                except:
                    pass

                # ---------------------------
                # STORE IN INDEX
                # ---------------------------
                index.append({
                    "name": file.lower(),
                    "path": file_path,
                    "type": file_type,
                    "functions": functions,
                    "apis": apis
                })

    return index


# ==============================
# STEP 2: SMART SEARCH
# ==============================
def search_relevant_files(ticket, index):

    ticket = ticket.lower()
    words = ticket.split()

    scored_files = []

    for file in index:
        if "test" in file["path"].lower():
         continue


        score = 0

        # ---------------------------
        # FILENAME MATCH
        # ---------------------------
        for word in words:
            if word in file["name"]:
                score += 2

        # ---------------------------
        # FILE TYPE PRIORITY
        # ---------------------------
        if file["type"] == "controller":
            score += 2
        elif file["type"] == "service":
            score += 1

        # ---------------------------
        # FUNCTION MATCH
        # ---------------------------
        for func in file["functions"]:
            for word in words:
                if word in func.lower():
                    score += 1

        # ---------------------------
        # API MATCH
        # ---------------------------
        for api in file["apis"]:
            for word in words:
                if word in api.lower():
                    score += 1

        # ---------------------------
        # CONTENT MATCH
        # ---------------------------
        try:
            with open(file["path"], "r", encoding="utf8", errors="ignore") as f:
                content = f.read().lower()

                for word in words:
                    if word in content:
                        score += 1
        except:
            pass

        if score > 0:
            scored_files.append((score, file["path"]))

    # ---------------------------
    # SORT + RETURN TOP 3
    # ---------------------------
    scored_files.sort(reverse=True)

    return [file for _, file in scored_files[:3]]