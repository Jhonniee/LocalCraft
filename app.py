import streamlit as st
from ProposalEngine import LeadCraftEngine

st.set_page_config(page_title="LeadCraft AI", page_icon="🚀", layout="wide")

st.title("⚡ LeadCraft AI: B2B Lead & Proposal Intelligence Engine")
st.markdown(
    "*Outperforming generic AI by matching real mathematical project relevance with high-converting proposal frameworks.*")

# Your Complete Real Portfolio Database
MY_PORTFOLIO = [
    {
        "title": "Netflix Content Intelligence & Machine Learning Suite",
        "description": "Engineered an end-to-end Python machine learning suite featuring TF-IDF content recommendation algorithms, 98.41% accurate binary classifiers, multi-class rating classifiers, K-Means customer segmentation, and linear regression trend forecasting."
    },
    {
        "title": "FixTogether Web Application",
        "description": "Independently designed and developed a fully responsive web application using HTML5, CSS3, and JavaScript, featuring clean user interface layout structures and client-side logic."
    },
    {
        "title": "Coderina Robotics & STEM Education Framework",
        "description": "Facilitated hands-on robotics and STEM programs using LEGO SPIKE Prime hardware, color sensors, motor control, and hardware-software integration logic for educational development."
    },
    {
        "title": "Java Object-Oriented Programming & Software Modules",
        "description": "Developed robust software logic applying Object-Oriented Programming principles, exception handling, data structures, and algorithmic execution in Java."
    }
]

engine = LeadCraftEngine(MY_PORTFOLIO)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Client Job Details")
    client_name = st.text_input("Client / Company Name (Optional):", placeholder="e.g. Flour Mills PLC, TechCorp")
    job_title = st.text_input("Job Role / Project Title:", placeholder="e.g. Senior Machine Learning Engineer")
    job_desc = st.text_area("Paste Client Job Description or Requirements:", height=200,
                            placeholder="Paste job specs here...")

    generate_btn = st.button("🚀 Match Portfolio & Generate Proposal", type="primary")

with col2:
    st.subheader("🎯 Match Analysis & Output")

    if generate_btn:
        if job_desc and job_title:
            with st.spinner("Analyzing semantics & ranking portfolio match..."):
                match = engine.find_best_match(job_desc)
                proposal = engine.generate_winning_proposal(client_name, job_title, job_desc, match)

                st.metric(label="Top Relevant Project Match", value=match['title'],
                          delta=f"{match['score']}% Match Confidence")

                st.markdown("### Generated Proposal Copy")
                st.code(proposal, language="markdown")

                # --- NEW: Export / Download Button ---
                st.download_button(
                    label="📥 Download Proposal (.txt)",
                    data=proposal,
                    file_name=f"Proposal_{client_name.replace(' ', '_') if client_name else 'Client'}.txt",
                    mime="text/plain"
                )

                st.success("Proposal ready to send and download!")
        else:
            st.error("Please enter both the Job Title and Job Description to proceed.")