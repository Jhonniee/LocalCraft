import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class LeadCraftEngine:
    def __init__(self, portfolio_items):
        self.df = pd.DataFrame(portfolio_items)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.portfolio_matrix = self.vectorizer.fit_transform(self.df['description'])

    def find_best_match(self, job_description):
        job_matrix = self.vectorizer.transform([job_description])
        scores = cosine_similarity(job_matrix, self.portfolio_matrix).flatten()

        best_index = scores.argmax()
        match_score = round(scores[best_index] * 100, 2)
        best_project = self.df.iloc[best_index]

        return {
            "title": best_project['title'],
            "description": best_project['description'],
            "score": match_score
        }

    def generate_winning_proposal(self, client_name, job_title, job_description, matched_project):
        proposal = f"""
Subject: High-impact solution for {job_title} | Proven track record

Hi {client_name if client_name else 'Hiring Team'},

I noticed you are looking for help with:
"{job_description[:160].strip()}..."

Rather than speaking in theory, I built an exact parallel solution: 
📌 **{matched_project['title']}**
• Impact & Logic: {matched_project['description']}

Key value I bring to your project:
1. End-to-end execution without micromanagement.
2. Production-ready code and clean architectural logic.
3. Rapid delivery aligned with your technical requirements.

Let's schedule a brief 10-minute call this week to review how we can implement this for your team immediately.

Best regards,
Aguiyi John Obichukwu
Lead AI & Software Engineer
        """
        return proposal.strip()