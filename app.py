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

# --- SIDEBAR MONETIZATION CONTROL CENTER ---
st.sidebar.title("🔐 User Account & Billing")

if not st.session_state.authenticated:
    st.sidebar.subheader("Login / Sign Up")
    user_email = st.sidebar.text_input("Email Address", placeholder="educator@school.com")
    if st.sidebar.button("Log In / Register"):
        if user_email:
            st.session_state.authenticated = True
            st.session_state.user_email = user_email
            st.rerun()
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.user_email}**")
    st.sidebar.write(f"Current Plan: **{st.session_state.user_tier}**")

    if st.session_state.user_tier == "Free":
        st.sidebar.write(f"Proposal Credits Remaining: **{st.session_state.credits}**")
        st.sidebar.markdown("---")
        st.sidebar.subheader("🚀 Upgrade Plan")

        # Strategy 1: B2B SaaS Subscription
        if st.sidebar.button("Subscribe Pro SaaS ($29/mo)"):
            st.session_state.user_tier = "Pro SaaS"
            st.success("Upgraded to Pro SaaS! Unlimited Proposals Unlocked.")
            st.rerun()

        # Strategy 3: Pay-Per-Proposal
        if st.sidebar.button("Buy 10 Credits ($15)"):
            st.session_state.credits += 10
            st.success("Added 10 Credits!")
            st.rerun()

        # Strategy 2: Enterprise White-Label
        if st.sidebar.button("Unlock Enterprise White-Label ($199)"):
            st.session_state.user_tier = "Enterprise White-Label"
            st.rerun()
    else:
        st.sidebar.success("Premium Tier Active: Unlimited Generations Enabled")

    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

# --- MAIN INTERFACE ---
st.title("⚡ LeadCraft AI: B2B STEM Proposal Engine")
st.caption("Generate high-converting commercial proposals, hardware allocations, and contracts in seconds.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Client Job Details")
    client_name = st.text_input(label="Client / Company Name:", placeholder="e.g., Bright Star Academy")
    job_title = st.text_input(label="Job Role / Project Title:", placeholder="e.g., STEM & Robotics Facilitator")
    job_desc = st.text_area(label="Paste Client Job Description or Requirements:",
                            placeholder="Paste job requirements here...")

    project_duration = st.text_input("Project Duration / Timeline:", placeholder="e.g., 3 Months")
    estimated_budget = st.text_input("Estimated Budget / Pricing Model:", placeholder="e.g., ₦150,000 / term")

    # Strategy 3: Equipment Breakout Feature
    hardware_kits = st.number_input("Hardware Kits to Allocate (LEGO SPIKE/Microcontrollers):", min_value=0, value=2)

    # Strategy 2: Enterprise White-Label Branding Field
    org_name = "LeadCraft Partner"
    if st.session_state.user_tier == "Enterprise White-Label":
        org_name = st.text_input("🏢 Custom Institution Name (White-Label):", value="Custom STEM Consulting Ltd")

    generate_btn = st.button(label="🚀 Generate Proposal & Calculate Match", type="primary")

with col2:
    st.subheader("🎯 Commercial Proposal Output")

    if generate_btn:
        if not st.session_state.authenticated:
            st.error("Please log in from the sidebar to generate proposals.")
        elif st.session_state.user_tier == "Free" and st.session_state.credits <= 0:
            st.error("Out of credits! Upgrade to Pro SaaS or purchase more credits in the sidebar.")
        elif job_desc:
            with st.spinner("Analyzing semantics and generating proposal..."):
                # Deduct credit if on Free plan
                if st.session_state.user_tier == "Free":
                    st.session_state.credits -= 1

                proposal_text, match_score = engine.generate_tailored_proposal(
                    client_name, job_title, job_desc, project_duration, estimated_budget, hardware_kits, org_name
                )

                st.metric(label="Match Relevance Index", value=f"{match_score}% Alignment")
                st.code(proposal_text, language="markdown")

                # PDF Generation
                pdf_bytes = engine.generate_pdf_proposal(proposal_text)

                st.download_button(
                    label="📄 Download Official PDF Proposal",
                    data=pdf_bytes,
                    file_name=f"Proposal_{client_name.replace(' ', '_') if client_name else 'Client'}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Please enter the client requirements first.")