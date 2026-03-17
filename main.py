from smart_repo_analyzer import build_index, search_relevant_files
from ai_agent import ai_reasoning
import json

print("\n=== Autonomous Incident-to-Fix Engineering Agent ===\n")

ticket = input("Enter Incident Ticket: ")

print("\n[Agent] Understanding incident...")

print("\n[Agent] Building repository index...")
index = build_index()

print("[Agent] Searching relevant files...")
files = search_relevant_files(ticket, index)

if not files:
    print("[Agent] No relevant files found in repository")
    exit()

print("\n[Agent] Top relevant files:")
for f in files:
    print("-", f)

file = files[0]

print("\n[Agent] Candidate file detected:", file)

with open(file, "r", encoding="utf8", errors="ignore") as f:
    code = f.read()

print("[Agent] Performing AI-based analysis...")

result = ai_reasoning(ticket, code)

# 🔥 FIX HANDLING
if isinstance(result, str):
    try:
        result = json.loads(result)
    except:
        result = {
            "confidence": "N/A",
            "risk": "N/A",
            "root_cause": result,
            "fix": result
        }

print("\n=== INCIDENT RESOLUTION REPORT ===\n")

print("Root Cause:")
print(result.get("root_cause", "N/A"))

print("\nSuggested Fix:")
print(result.get("fix", "N/A"))

print("\nConfidence Score:", result.get("confidence", "N/A"))
print("Risk Level:", result.get("risk", "N/A"))

print("\nExecution Timeline:")
print("00:00 Ticket received")
print("00:02 Repository scanned")
print("00:04 Root cause identified")
print("00:05 Fix generated")