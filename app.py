import streamlit as st
from ProposalEngine import LeadCraftEngine

st.set_page_config(page_title="LeadCraft AI - Commercial B2B Engine", layout="wide", page_icon="⚡")

# Initialize Engine
engine = LeadCraftEngine()

# --- USER SESSION & MONETIZATION STATE SIMULATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_tier" not in st.session_state:
    st.session_state.user_tier = "Free"
if "credits" not in st.session_state:
    st.session_state.credits = 3  # 3 Free trial credits

# --- FULL PAGE LOGIN & BILLING WALL ---
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

    # Stops Streamlit from loading the proposal tools below until logged in
    st.stop()

# =========================================================
# --- MAIN APP (Only visible AFTER successful login) ---
# =========================================================

# Top Navigation / User Banner
st.sidebar.title("👤 Account & Billing")
st.sidebar.write(f"Logged in as: **{st.session_state.get('user_email', 'User')}**")
st.sidebar.write(f"Plan: **{st.session_state.user_tier}** | Credits: **{st.session_state.credits}**")

if st.sidebar.button("Log Out"):
    st.session_state.authenticated = False
    st.rerun()

# Your existing Proposal Generator Code below this line:
st.title("🚀 LeadCraft AI - Commercial B2B Engine")
# ... (paste your job description inputs and generate buttons here)