from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import io


class LeadCraftEngine:
    def __init__(self, portfolio=None):
        raw_portfolio = portfolio if portfolio is not None else [
            "Hands-on LEGO SPIKE Prime and SPIKE Essential robotics curriculum for middle school and high school students focusing on microcontrollers, sensors, and mechanical assembly.",
            "B2B technical training bootcamps, instructor training, and STEM lab setup for private educational institutions and academies.",
            "Python automation, data literacy, and software logic training for institutional teams and students.",
            "Java programming and Object-Oriented Programming (OOP) fundamentals training, software logic structuring, and practical coding exercises.",
            "Information technology fundamentals, networking basics, and structured technical support training programs for schools and corporate organizations.",
            "Custom STEM project-based learning design, student progress reporting frameworks, and final showcase project mentorship."
        ]

        self.portfolio_projects = []
        for item in raw_portfolio:
            if isinstance(item, dict):
                text = item.get("description", item.get("desc", str(item)))
                self.portfolio_projects.append(text)
            else:
                self.portfolio_projects.append(str(item))

        self.vectorizer = TfidfVectorizer()

    def calculate_match_score(self, client_requirements):
        corpus = self.portfolio_projects + [str(client_requirements)]
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        best_score = float(similarity_scores.max()) * 100
        return round(best_score, 2)

    def generate_tailored_proposal(self, client_name, project_title, client_requirements, duration, budget,
                                   hardware_kits=0, organization_name="LeadCraft AI Partner"):
        match_score = self.calculate_match_score(client_requirements)

        hardware_section = ""
        if hardware_kits > 0:
            hardware_section = f"""
## 3. Hardware Deployment & Logistics
* **Robotics/STEM Kits Allocated:** {hardware_kits} Reusable Kit(s) (LEGO SPIKE / Microcontrollers)
* **Logistics & Asset Assurance:** Equipment provided under institutional loan agreement with maintenance support included.
"""

        proposal = f"""
================================================================================
                            COMMERCIAL PROPOSAL
                             {organization_name.upper()}
================================================================================

Prepared for: {client_name if client_name else "Valued Institutional Partner"}  
Project Scope: {project_title}  
Match Relevance Index: {match_score}% Technical Alignment  

--------------------------------------------------------------------------------
1. EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
We are pleased to submit this commercial technical proposal for {client_name if client_name else "your organization"}.
Based on your requirements:
"{client_requirements[:120]}..."

Our framework delivers practical, high-impact facilitation engineered to bridge institutional 
learning gaps and optimize operational productivity.

--------------------------------------------------------------------------------
2. PROPOSED TIMELINE & DELIVERY STRUCTURE
--------------------------------------------------------------------------------
* Estimated Duration: {duration if duration else "Flexible / Term-based"}
* Execution Model: On-site practical facilitation, continuous evaluation, and project showcases.
{hardware_section}
--------------------------------------------------------------------------------
4. FINANCIAL FRAMEWORK & INVESTMENT
--------------------------------------------------------------------------------
* Pricing Structure: {budget if budget else "Competitive Retainer Model"}
* Value Assurance: Asset-light deployment ensures minimal institutional overhead while maximizing outcome quality.

--------------------------------------------------------------------------------
5. NEXT STEPS & ENGAGEMENT
--------------------------------------------------------------------------------
To confirm this scope, we propose an initial alignment session to map schedule dates and hardware deployment.
"""
        return proposal, match_score

    def generate_pdf_proposal(self, text_proposal):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        for line in text_proposal.split('\n'):
            pdf.cell(0, 6, txt=line.encode('latin-1', 'replace').decode('latin-1'), ln=True)

        return pdf.output(dest='S').encode('latin-1')