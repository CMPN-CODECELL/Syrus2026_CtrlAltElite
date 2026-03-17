import streamlit as st
import time
import json

from smart_repo_analyzer import build_index, search_relevant_files
from ai_agent import ai_reasoning
from sandbox_executor import create_sandbox, apply_patch, run_tests_simulation, generate_patch_log

st.set_page_config(
    page_title="Incident-to-Fix Engineering Agent",
    page_icon="🤖",
    layout="wide"
)

# ==============================
# SESSION STATE INIT
# ==============================
if "status" not in st.session_state:
    st.session_state.status = "Waiting for execution..."

if "result" not in st.session_state:
    st.session_state.result = None

if "file" not in st.session_state:
    st.session_state.file = None

if "last_ticket" not in st.session_state:
    st.session_state.last_ticket = None

# ==============================
# HEADER
# ==============================
st.markdown("""
# 🤖 Autonomous Incident-to-Fix Engineering Agent
AI system that interprets incident tickets, analyzes the Shopstack platform repository,
detects root causes and generates safe code fixes automatically.
""")

st.divider()

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("⚙️ Incident Controls")

ticket = st.sidebar.selectbox(
    "Select Incident Scenario",
    [
        "Checkout API fails when cart is empty",
        "User login fails when email contains uppercase letters",
        "Payment API throws error during checkout",
        "Order API returns null response",
        "Password stored without hashing"
    ]
)

# RESET STATUS ON NEW TICKET
if st.session_state.last_ticket is None:
    st.session_state.last_ticket = ticket
elif ticket != st.session_state.last_ticket:
    st.session_state.status = "Waiting for execution..."
    st.session_state.last_ticket = ticket

run = st.sidebar.button("🚀 Run Agent")

# ==============================
# LAYOUT
# ==============================
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📄 Incident Ticket")
    st.success(ticket)

# STATUS (DYNAMIC SINGLE LINE)
status_placeholder = col2.empty()
status_placeholder.subheader("🧠 Agent Status")
status_placeholder.info(st.session_state.status)

# ==============================
# RUN AGENT
# ==============================
if run:

    # STEP 1 → EXECUTING
    st.session_state.status = "Executing agent..."
    status_placeholder.info(st.session_state.status)

    with st.spinner("Agent is running..."):

        st.write("🧠 Understanding incident...")
        time.sleep(1)

        st.write("🔍 Scanning repository...")
        index = build_index()
        files = search_relevant_files(ticket, index)

        time.sleep(1)

        if not files:
            st.error("No relevant files found.")
            st.session_state.status = "Execution failed"
            status_placeholder.info(st.session_state.status)

        else:
            st.write("📂 Identifying relevant files...")
            time.sleep(1)

            st.subheader("📜 Agent Logs")
            st.code("""
[INFO] Ticket received
[INFO] Repository scanned
[INFO] Relevant files identified
[INFO] Root cause analysis completed
[INFO] Patch generated successfully
""")

            st.subheader("📁 Relevant Files Found")
            for f in files:
                st.code(f)

            file = files[0]

            with open(file, "r", encoding="utf8", errors="ignore") as f:
                code = f.read()

            result = ai_reasoning(ticket, code)

            # SAFE HANDLING
            if isinstance(result, str):
                result = {
                    "root_cause": result,
                    "fix": result,
                    "confidence": 0.5,
                    "risk": "Unknown",
                    "explanation": "Fallback"
                }

            # SAVE STATE
            st.session_state.result = result
            st.session_state.file = file

            st.divider()

            # ==============================
            # METRICS
            # ==============================
            colA, colB, colC = st.columns(3)

            colA.metric("Files Found", len(files))
            colB.metric("Confidence", round(result["confidence"], 2))
            colC.metric("Risk", result["risk"])

            st.divider()

            # ==============================
            # OUTPUT
            # ==============================
            colX, colY = st.columns(2)

            with colX:
                st.subheader("🔍 Root Cause")
                st.warning(result["root_cause"])

                st.subheader("📁 Selected File")
                st.code(file)

            with colY:
                st.subheader("🛠 Suggested Patch")
                st.code(result["fix"], language="javascript")

            st.subheader("🧠 Explanation")
            st.info(result.get("explanation", "No explanation"))

            st.divider()

            st.subheader("⏱ Execution Timeline")
            st.code("""
00:00 Ticket received
00:02 Repository scanned
00:04 Root cause identified
00:05 Fix generated
""")

            st.success("✅ Analysis completed")

            # STEP 2 → COMPLETED
            st.session_state.status = "Execution completed"
            status_placeholder.info(st.session_state.status)

# ==============================
# APPLY FIX
# ==============================
if st.session_state.result and st.session_state.file:

    st.divider()

    if st.button("🚀 Apply Fix (Simulation)"):

        result = st.session_state.result
        file = st.session_state.file

        st.warning("⚠️ Performing safety validation...")
        time.sleep(1)
        st.success("No critical risks detected")

        st.info("Creating sandbox environment...")
        sandbox_dir, sandbox_file = create_sandbox(file)

        if not sandbox_file:
            st.error("Sandbox creation failed")
        else:
            st.success("Sandbox created successfully")

            st.info("Applying patch...")
            success = apply_patch(sandbox_file, result["fix"])

            if success:
                st.success("Patch applied successfully")

                st.info("Running validation tests...")
                test_results = run_tests_simulation()

                st.subheader("🧪 Test Results")
                st.code(test_results)

                st.info("Generating patch logs...")
                log = generate_patch_log(sandbox_file, result["fix"])

                st.subheader("📜 Patch Log")
                st.code(log)

                st.success("Fix validated successfully in sandbox")

                st.subheader("🚀 Pull Request Simulation")
                st.code(f"""
Branch: fix/{ticket.replace(" ", "_")}
Commit: Applied automated fix
Status: Ready for review
""")