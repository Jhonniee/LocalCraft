import streamlit as st
# Import your proposal engine (make sure ProposalEngine.py is in the same folder)
from ProposalEngine import LeadCraftEngine

st.set_page_config(page_title="LeadCraft AI - Commercial B2B Engine", layout="wide")

# Initialize Engine
engine = LeadCraftEngine()

# --- 1. INITIALIZE SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_tier" not in st.session_state:
    st.session_state.user_tier = "Free"
if "credits" not in st.session_state:
    st.session_state.credits = 3  # Free trial credits

# --- 2. LOGIN & BILLING GATE (First Page Seen) ---
if not st.session_state.authenticated:
    st.title("👤 User Account & Billing")
    st.write("Welcome to **LeadCraft AI**. Please enter your email to sign in and access your proposal generator.")

    with st.form("login_form"):
        user_email = st.text_input("Email Address", placeholder="educator@school.com")
        submit_btn = st.form_submit_button("Log In / Register")

        if submit_btn:
            if user_email:
                st.session_state.authenticated = True
                st.session_state.user_email = user_email
                st.success("Access granted!")
                st.rerun()
            else:
                st.error("Please enter a valid email address.")

    st.info(
        f"💡 **Current Plan:** {st.session_state.user_tier} Tier | **Credits Remaining:** {st.session_state.credits}")

    # Stops Streamlit from loading the app below until logged in
    st.stop()

# =========================================================
# --- 3. MAIN APP (Only visible AFTER successful login) ---
# =========================================================

# Sidebar Account & Billing Info
st.sidebar.title("👤 Account & Billing")
st.sidebar.write(f"Logged in as: **{st.session_state.user_email}**")
st.sidebar.write(f"Current Plan: **{st.session_state.user_tier}**")
st.sidebar.write(f"Proposal Credits Remaining: **{st.session_state.credits}**")

if st.sidebar.button("Upgrade Plan"):
    st.sidebar.info("Subscribe Pro SaaS ($29/mo) or Buy 10 Credits ($15)")

if st.sidebar.button("Log Out"):
    st.session_state.authenticated = False
    st.rerun()

# --- Main Proposal Generator UI ---
st.title("🚀 LeadCraft AI - Commercial B2B Engine")
st.write("Generate tailored, professional project proposals and cost estimates instantly.")

# Input fields for your proposal generator
client_job = st.text_area("Paste Client Job Description or Requirements:",
                          placeholder="e.g., We need an interactive web platform and STEM robotics curriculum...")
project_duration = st.text_input("Project Duration / Timeline:", placeholder="e.g., 3 Months")
estimated_budget = st.text_input("Estimated Budget / Pricing Model:", placeholder="e.g., ₦150,000 / term")
hardware_kits = st.number_input("Hardware Kits to Allocate (LEGO SPIKE/Microcontrollers):", min_value=0, value=2)

if st.button("Generate Proposal & Calculate Match"):
    if client_job and st.session_state.credits > 0:
        with st.spinner("Generating professional proposal..."):
            # Deduct credit and generate
            st.session_state.credits -= 1

            # Call your backend engine
            proposal_output = engine.generate_proposal(client_job, project_duration, estimated_budget)

            st.subheader("📄 Generated Proposal")
            st.write(proposal_output)
            st.success("Proposal generated successfully! 1 credit deducted.")
    elif st.session_state.credits <= 0:
        st.error("You have run out of credits! Please upgrade your plan in the sidebar.")
    else:
        st.warning("Please paste the client job description first.")