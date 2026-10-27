from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class LeadCraftEngine:
    def __init__(self, portfolio=None):
        # Sample portfolio or core competencies database
        if portfolio is not None:
            self.portfolio_projects = portfolio
        else:
            self.portfolio_projects = [
                "Hands-on LEGO SPIKE robotics and coding curriculum for middle school students focusing on microcontrollers and sensors.",
                "B2B technical training bootcamps and STEM lab setup for private educational institutions.",
                "Python automation, data literacy, and software logic training for institutional teams."
            ]
        self.vectorizer = TfidfVectorizer()

    def calculate_match_score(self, client_requirements):
        """Uses TF-IDF to calculate relevance score between client needs and your portfolio."""
        corpus = self.portfolio_projects + [client_requirements]
        tfidf_matrix = self.vectorizer.fit_transform(corpus)

        # Calculate cosine similarity between the last document (client needs) and portfolio
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        best_score = float(similarity_scores.max()) * 100
        return round(best_score, 2)

    def generate_tailored_proposal(self, client_name, project_title, client_requirements, duration, budget):
        match_score = self.calculate_match_score(client_requirements)

        proposal = f"""
# COMMERCIAL PROPOSAL & SERVICE AGREEMENT
**Prepared for:** {client_name if client_name else "Valued Institutional Partner"}  
**Project Scope:** {project_title}  
**Match Relevance Index:** {match_score}% Alignment  

---

## 1. Executive Summary
We are pleased to submit this tailored technical service proposal for **{client_name if client_name else "your organization"}**. Based on your requirements (*"{client_requirements[:100]}..."*), our framework delivers high-impact, practical execution designed to bridge the technical learning and operational gap efficiently.

## 2. Proposed Timeline & Delivery Structure
* **Estimated Duration:** {duration if duration else "Flexible / Structured per Term"}
* **Execution Model:** On-site practical facilitation combined with continuous progress tracking and milestone reviews.
* **Resource Commitment:** Fully equipped with reusable hardware assets, standardized curriculum modules, and dedicated instruction.

## 3. Financial Framework & Investment
* **Pricing Model:** {budget if budget else "Competitive B2B Retainer / Term-based Structure"}
* **Value Assurance:** Asset-light deployment ensures minimal institutional overhead while maximizing student/operational engagement.

## 4. Next Steps
To confirm this engagement and schedule setup, we propose a brief alignment meeting to review equipment readiness and finalize the implementation calendar.
        """
        return proposal