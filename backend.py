import google.generativeai as genai
import requests
import streamlit as st
import json

def configure_apis():
    """Configures the Gemini API using secrets."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        else:
            st.error("GEMINI_API_KEY not found in secrets.")
    except Exception as e:
        st.error(f"Error configuring APIs: {e}")

def analyze_resume(uploaded_file):
    """
    Analyzes the uploaded resume using Gemini Vision.
    Returns a summary string.
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Read file bytes and determine mime type
        file_bytes = uploaded_file.getvalue()
        mime_type = uploaded_file.type
        
        prompt = "Extract Name, Skills, Experience, and Preferred Roles into a summary."
        
        # Pass the file bytes directly to the model
        response = model.generate_content([
            {'mime_type': mime_type, 'data': file_bytes},
            prompt
        ])
        
        return response.text
    except Exception as e:
        st.error(f"Error analyzing resume: {e}")
        return None

def generate_search_query(user_input):
    """
    Translates natural language input into a structured Google Search query.
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Translate the following user job search request into a precise Google Search query.
        
        CRITICAL RULES:
        1. Target ONLY job listing paths: site:linkedin.com/jobs OR site:naukri.com OR site:indeed.com
        2. Append these negative keywords to exclude articles and salary info: -salary -average -trends -articles -"how much"
        3. Keep the query focused on the role and location.
        
        User Input: "{user_input}"
        
        Output ONLY the search query string.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating search query: {e}")
        return None

def search_jobs(query):
    """
    Searches for jobs using Google Custom Search JSON API.
    Returns a list of dictionaries with Title, Link, and Snippet.
    Filters out non-job results and limits to 5 items.
    """
    try:
        if "GOOGLE_SEARCH_API_KEY" not in st.secrets or "SEARCH_ENGINE_ID" not in st.secrets:
            st.error("Google Search API keys missing in secrets.")
            return []

        api_key = st.secrets["GOOGLE_SEARCH_API_KEY"]
        cx = st.secrets["SEARCH_ENGINE_ID"]
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cx,
            "q": query,
            "num": 8 # Fetch buffer to allow for filtering
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        filtered_results = []
        forbidden_words = ["salary", "average", "how much", "trends", "articles"]
        
        if "items" in data:
            for item in data["items"]:
                title = item.get("title", "").lower()
                snippet = item.get("snippet", "").lower()
                
                # Filter logic
                if any(word in title for word in forbidden_words) or any(word in snippet for word in forbidden_words):
                    continue
                    
                filtered_results.append({
                    "Title": item.get("title"),
                    "Link": item.get("link"),
                    "Snippet": item.get("snippet")
                })
        
        # Hard limit to 5
        return filtered_results[:5]
        
    except Exception as e:
        st.error(f"Error searching jobs: {e}")
        return []

def analyze_job_match(resume_summary, job_details):
    """
    Compares resume summary with job details using Gemini.
    Returns a JSON object: {"score": int, "reason": "string"}
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash", generation_config={"response_mime_type": "application/json"})
        
        prompt = f"""
        Act as a Strict Recruiter. Compare the following Resume Summary with the Job Details.
        
        Resume Summary:
        {resume_summary}
        
        Job Details:
        {job_details}
        
        Provide a match score (0-100) and a concise reason.
        Output MUST be valid JSON in the format: {{"score": int, "reason": "string"}}
        """
        
        response = model.generate_content(prompt)
        
        # Robust JSON parsing: strip markdown
        text_response = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text_response)
    except Exception as e:
        st.error(f"Error analyzing job match: {e}")
        return {"score": 0, "reason": "Error during analysis"}

def generate_application_kit(resume_summary, job_title, company_name):
    """
    Generates a professional cover letter.
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Write a professional cover letter for the position of {job_title} at {company_name}.
        Use the following resume summary to highlight relevant skills and experience:
        {resume_summary}
        
        Keep it professional, engaging, and concise.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating application kit: {e}")
        return "Could not generate cover letter."

def create_pdf(text):
    """
    Converts text to a PDF file bytes.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from io import BytesIO
        import html

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create a custom style for the body text
        style = ParagraphStyle(
            name='Normal',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            spaceAfter=12
        )
        
        story = []
        
        # Process text: escape HTML and handle newlines
        # We split by newlines to create separate paragraphs for better formatting
        paragraphs = text.split('\n')
        
        for para in paragraphs:
            if para.strip():
                # Escape HTML characters to prevent errors
                safe_text = html.escape(para)
                # Basic markdown bold handling (very simple)
                safe_text = safe_text.replace('**', '<b>', 1).replace('**', '</b>', 1)
                story.append(Paragraph(safe_text, style))
            else:
                story.append(Spacer(1, 12))
                
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Error creating PDF: {e}")
        return None
