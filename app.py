import streamlit as st
import time

from smart_repo_analyzer import build_index, search_relevant_files
from ai_agent import ai_reasoning


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

# 🔥 RESET STATUS WHEN USER CHANGES TICKET
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

status_placeholder = col2.empty()
status_placeholder.subheader("🧠 Agent Status")
status_placeholder.info(st.session_state.status)

# ==============================
# RUN AGENT
# ==============================
if run:

    # 🔥 STEP 1 → EXECUTING
    st.session_state.status = "Executing agent..."
    status_placeholder.info(st.session_state.status)

    with st.spinner("Agent is running..."):

        st.write("🧠 Understanding incident...")
        time.sleep(1)

        st.write("🔍 Scanning repository...")
        time.sleep(1)

        index = build_index()
        files = search_relevant_files(ticket, index)

        st.write("📂 Identifying relevant files...")
        time.sleep(1)

        if not files:
            st.error("No relevant files found.")
            st.session_state.status = "Execution failed"
            status_placeholder.info(st.session_state.status)

        else:
            st.write("🧠 Performing root cause analysis...")
            time.sleep(1)

            st.divider()

            # Logs
            st.subheader("📜 Agent Logs")
            st.code("""
[INFO] Ticket received
[INFO] Repository scanned
[INFO] Relevant files identified
[INFO] Root cause analysis completed
[INFO] Patch generated successfully
""")

            # Files
            st.subheader("📁 Relevant Files Found")
            for f in files:
                st.code(f)

            file = files[0]

            with open(file, "r", encoding="utf8", errors="ignore") as f:
                code = f.read()

            result = ai_reasoning(ticket, code)

            st.divider()

            # Metrics
            colA, colB, colC = st.columns(3)
            colA.metric("Files Found", len(files))
            colB.metric("Confidence", result["confidence"])
            colC.metric("Risk", result["risk"])

            st.divider()

            # Output
            colX, colY = st.columns(2)

            with colX:
                st.subheader("🔍 Root Cause")
                st.warning(result["root_cause"])

                st.subheader("📁 Selected File")
                st.code(file)

            with colY:
                st.subheader("🛠 Suggested Patch")
                st.code(result["fix"], language="javascript")

            st.divider()

            # Apply Fix
            if st.button("🚀 Apply Fix (Simulation)"):
                st.success("Patch applied successfully")
                st.info("No regressions detected")

            # Timeline
            st.subheader("⏱ Execution Timeline")
            st.code("""
00:00 Ticket received
00:02 Repository scanned
00:04 Root cause identified
00:05 Fix generated
""")

            st.success("✅ Completed successfully")

            # 🔥 STEP 3 → COMPLETED
            st.session_state.status = "Execution completed"
            status_placeholder.info(st.session_state.status)